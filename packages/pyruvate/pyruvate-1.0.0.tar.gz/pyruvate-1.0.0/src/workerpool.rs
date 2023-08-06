use cpython::{PyClone, PyObject, Python};
use crossbeam_channel::{unbounded, Receiver, SendError, Sender};
use mio::Token;
use threadpool::ThreadPool;

use crate::globals::{ServerOptions, SharedWSGIOptions};
use crate::request::WSGIRequest;
use crate::transport::{Connection, HTTP11Connection};

pub const MARKER: Token = Token(0);
pub type WorkerPayload<T> = (WSGIRequest, Option<HTTP11Connection<T>>);
type SendResult<T> = Result<(), SendError<(Token, WorkerPayload<T>)>>;

pub struct WorkerPool<T: Connection> {
    workers: ThreadPool,
    application: PyObject,
    input: Sender<(Token, WorkerPayload<T>)>,
    pub reusable_connections: Receiver<(Token, HTTP11Connection<T>)>,
}

impl<T: 'static + Connection + Sync> WorkerPool<T> {
    pub fn new<F>(
        options: &ServerOptions,
        application: PyObject,
        worker: F,
        py: Python,
    ) -> WorkerPool<T>
    where
        F: 'static
            + Fn(
                usize,
                SharedWSGIOptions,
                PyObject,
                Receiver<(Token, (WSGIRequest, Option<HTTP11Connection<T>>))>,
                Sender<(Token, HTTP11Connection<T>)>,
            )
            + Send
            + Copy,
    {
        let (input, rcv) = unbounded::<(Token, WorkerPayload<T>)>();
        let (snd, reusable_connections) = unbounded::<(Token, HTTP11Connection<T>)>();
        let wp = WorkerPool {
            application,
            workers: ThreadPool::new(options.num_workers),
            input,
            reusable_connections,
        };
        for idx in 0..options.num_workers {
            let rcv = rcv.clone();
            let threadapp = wp.application.clone_ref(py); // "Clone self, Calls Py_INCREF() on the ptr."
            let wi = options.wsgi_options.clone();
            let snd = snd.clone();
            wp.workers.execute(move || {
                worker(idx, wi, threadapp, rcv, snd);
            });
        }
        wp
    }

    pub fn execute(
        &mut self,
        token: Token,
        req: WSGIRequest,
        out: Option<HTTP11Connection<T>>,
    ) -> SendResult<T> {
        self.input.send((token, (req, out)))
    }

    pub fn join(&mut self) -> SendResult<T> {
        for _ in 0..self.workers.max_count() {
            self.execute(MARKER, WSGIRequest::new(0, String::new()), None)?;
        }
        self.workers.join();
        Ok(())
    }
}

#[cfg(test)]
mod tests {
    use cpython::{PyClone, PyDict, Python, PythonObject};
    use log::debug;
    use mio::net::{TcpListener, TcpStream};
    use mio::Token;
    use python3_sys::{PyEval_RestoreThread, PyEval_SaveThread};
    use std::time::Duration;

    use crate::globals::{shared_wsgi_options, ServerOptions, SharedWSGIOptions};
    use crate::request::WSGIRequest;
    use crate::transport::shared_connection_options;
    use crate::workerpool::WorkerPool;
    use crate::workers::{write_blocking_worker, write_non_blocking_worker};

    fn server_options(globals: SharedWSGIOptions) -> ServerOptions {
        ServerOptions {
            num_workers: 2,
            write_blocking: false,
            max_number_headers: 16,
            connection_options: shared_connection_options(10, Duration::from_secs(60)),
            wsgi_options: globals,
        }
    }

    #[test]
    fn test_pool_simple_blocking() {
        let gil = Python::acquire_gil();
        let py = gil.python();
        let server_name = String::from("127.0.0.1");
        let port = String::from("0");
        let sn = "/foo";
        let locals = PyDict::new(py);
        let app = py.run(
            r#"
def simple_app(environ, start_response):
    status = '200 OK'
    response_headers = [('Content-type', 'text/plain'), ("Expires", "Sat, 1 Jan 2000 00:00:00 GMT")]
    start_response(status, response_headers)
    return [b"Hello world!\n"]

app = simple_app"#,
            None,
            Some(&locals),
        );
        match app {
            Ok(_) => {
                let app = locals
                    .get_item(py, "app")
                    .unwrap()
                    .as_object()
                    .clone_ref(py);
                let raw = b"GET /foo42?bar=baz HTTP/1.1\r\nHost: localhost:7878\r\nUser-Agent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:70.0) Gecko/20100101 Firefox/70.0\r\nAccept: image/webp,*/*\r\nAccept-Language: de-DE,en-US;q=0.7,en;q=0.3\r\nAccept-Encoding: gzip, deflate\r\nConnection: keep-alive\r\nCookie: foo_language=en;\r\nDNT: 1\r\n\r\n";
                let mut req1 = WSGIRequest::new(16, String::new());
                req1.append(raw);
                req1.parse_data();
                let mut req2 = WSGIRequest::new(16, String::new());
                req2.append(raw);
                req2.parse_data();
                let mut req3 = WSGIRequest::new(16, String::new());
                req3.append(raw);
                req3.parse_data();
                let mut req4 = WSGIRequest::new(16, String::new());
                req4.append(raw);
                req4.parse_data();
                let mut wp = WorkerPool::<TcpStream>::new(
                    &server_options(shared_wsgi_options(
                        server_name,
                        port,
                        sn.to_string(),
                        false,
                        py,
                    )),
                    app,
                    write_blocking_worker::<TcpListener, TcpStream>,
                    py,
                );
                let token = Token(42);
                let py_thread_state = unsafe { PyEval_SaveThread() };
                wp.execute(token, req1, None).unwrap();
                wp.execute(token, req2, None).unwrap();
                wp.execute(token, req3, None).unwrap();
                wp.execute(token, req4, None).unwrap();
                match wp.join() {
                    Ok(_) => debug!("wp joined"),
                    Err(_) => {
                        debug!("Could not join workers");
                        assert!(false);
                    }
                }
                unsafe { PyEval_RestoreThread(py_thread_state) };
            }
            Err(e) => {
                debug!("Error encountered: {:?}", e);
                e.print_and_set_sys_last_vars(py);
                assert!(false);
            }
        }
    }

    #[test]
    fn test_pool_simple_non_blocking() {
        let gil = Python::acquire_gil();
        let py = gil.python();
        let server_name = String::from("127.0.0.1");
        let port = String::from("0");
        let sn = "/foo";
        let locals = PyDict::new(py);
        let app = py.run(
            r#"
def simple_app(environ, start_response):
    status = '200 OK'
    response_headers = [('Content-type', 'text/plain'), ("Expires", "Sat, 1 Jan 2000 00:00:00 GMT")]
    start_response(status, response_headers)
    return [b"Hello world!\n"]

app = simple_app"#,
            None,
            Some(&locals),
        );
        match app {
            Ok(_) => {
                let app = locals
                    .get_item(py, "app")
                    .unwrap()
                    .as_object()
                    .clone_ref(py);
                let raw = b"GET /foo42?bar=baz HTTP/1.1\r\nHost: localhost:7878\r\nUser-Agent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:70.0) Gecko/20100101 Firefox/70.0\r\nAccept: image/webp,*/*\r\nAccept-Language: de-DE,en-US;q=0.7,en;q=0.3\r\nAccept-Encoding: gzip, deflate\r\nConnection: keep-alive\r\nCookie: foo_language=en;\r\nDNT: 1\r\n\r\n";
                let mut req1 = WSGIRequest::new(16, String::new());
                req1.append(raw);
                req1.parse_data();
                let mut req2 = WSGIRequest::new(16, String::new());
                req2.append(raw);
                req2.parse_data();
                let mut req3 = WSGIRequest::new(16, String::new());
                req3.append(raw);
                req3.parse_data();
                let mut req4 = WSGIRequest::new(16, String::new());
                req4.append(raw);
                req4.parse_data();
                let mut wp = WorkerPool::<TcpStream>::new(
                    &server_options(shared_wsgi_options(
                        server_name,
                        port,
                        sn.to_string(),
                        false,
                        py,
                    )),
                    app,
                    write_non_blocking_worker::<TcpListener, TcpStream>,
                    py,
                );
                let token = Token(42);
                let py_thread_state = unsafe { PyEval_SaveThread() };
                wp.execute(token, req1, None).unwrap();
                wp.execute(token, req2, None).unwrap();
                wp.execute(token, req3, None).unwrap();
                wp.execute(token, req4, None).unwrap();
                match wp.join() {
                    Ok(_) => debug!("wp joined"),
                    Err(_) => {
                        debug!("Could not join workers");
                        assert!(false);
                    }
                }
                unsafe { PyEval_RestoreThread(py_thread_state) };
            }
            Err(e) => {
                debug!("Error encountered: {:?}", e);
                e.print_and_set_sys_last_vars(py);
                assert!(false);
            }
        }
    }
}
