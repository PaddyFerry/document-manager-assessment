// import React, { useState, useEffect } from "react";
//
// import "./FileVersions.css";
// import {ChangeEvent} from "react";
//
// function Login() {
//
//     const onSubmit = (data) => console.log(data);
//     const url = "http://localhost:8001/auth-token/"
//
//   return (
//       <div>
//       <h3> Login Form </h3>
//           <form className="Login" onSubmit={onSubmit}>
//               <div className="email-field">Email<input type="email"/></div>
//               <div>Password <input type="password"/></div>
//
//               <button type="submit">Login</button>
//           </form>
//       </div>
//   );
// }
//
// // function FileUpload(props) {
// //     const [file, setFile] = useState()
// //
// //   function handleChange(event) {
// //     setFile(event.target.files[0])
// //   }
//
// // function handleSubmit(event) {
// //         console.log("FILE UPLOADED")
// //         event.preventDefault()
// //         const url = 'http://localhost:8001/api/files/';
// //         const formData = new FormData();
// //         formData.append('file', file);
// //         // formData.append('fileName', file.name);
// //         formData.append('location', window.location.pathname || "/");
// //     fetch(url,
// //             {
// //                 method: "POST",
// //                 headers: new Headers({
// //                     Authorization: 'Token 17f914ca39030d6d0907f4d342c4627d1b17b038',
// //                     // 'content-type': 'multipart/form-data'
// //                 }),
// //                 body: formData
// //             }
// //         );
// //   }
// //
// //   return (
// //       <div className="file-upload">
// //           <form onSubmit={handleSubmit}>
// //               <h3>Upload file</h3>
// //               <input type="file" onChange={handleChange} />
// //               <button type="submit">Upload</button>
// //           </form>
// //       </div>
// //   );
// // }
//
//
// // function FileVersions() {
// //     const [data, setData] = useState([]);
// //   // console.log(data);
// //   // console.log(window.location.pathname);
// //
// //   useEffect(() => {
// //     // fetch data
// //     const dataFetch = async () => {
// //       const data = await (
// //         await fetch(`http://localhost:8001/api/files/?` + new URLSearchParams({
// //             location: window.location.pathname || "/"
// //         }),
// //             {
// //                 method: "GET",
// //
// //                 headers: new Headers({
// //                     Authorization: 'Token 17f914ca39030d6d0907f4d342c4627d1b17b038',
// //     }),
// //             }
// //         )
// //       ).json();
// //
// //       // set state when the data received
// //       setData(data);
// //     };
//
// //     dataFetch();
// //   }, []);
// //   return (
// //     <div>
// //       <h2>Login</h2>
// //         <Login></Login>
// //
// //     </div>
// //   );
// // }
//
// export default Login;
