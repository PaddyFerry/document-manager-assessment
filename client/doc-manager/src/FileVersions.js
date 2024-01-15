import React, { useState, useEffect } from "react";

import "./FileVersions.css";
import {ChangeEvent} from "react";
import {Box, Button} from "@mui/material";
import Stack from '@mui/material/Stack';

function FileVersionsList(props) {
  const file_versions = props.file_versions;
  let files = file_versions.map((file_version) => (

    <Box className="file-version" key={file_version.id}>

      <h2>{file_version.file_name + "." + file_version.extension}</h2>
      <p>
        Version: {file_version.version_number}<br/>
          <Button variant="contained" href={`http://localhost:8001/api/files/${file_version.id}/download/`}>Download</Button>
      </p>
    </Box>
  ));
  return <Stack>{files}</Stack>
}

function FileUpload() {
    const [file, setFile] = useState()

  function handleChange(event) {
    setFile(event.target.files[0])
  }

    function handleSubmit(event) {
        event.preventDefault()
        const url = 'http://localhost:8001/api/files/';
        const formData = new FormData();
        formData.append('file', file);
        console.log(file.name)
        // formData.append('fileName', file.name);
        formData.append('location', window.location.pathname || "/");
        fetch(url,
            {
                method: "POST",
                headers: new Headers({
                    Authorization: 'Token 17f914ca39030d6d0907f4d342c4627d1b17b038',
                    // 'content-type': 'multipart/form-data'
                }),
                body: formData
            }
        );
  }

  return (
      <div className="file-upload">
          <form onSubmit={handleSubmit}>
              <h3>Upload file</h3>
              <input type="file" onChange={handleChange} />
              <Button type="submit" variant="contained" >Upload</Button>
          </form>
      </div>
  );
}


function FileVersions() {
    const [data, setData] = useState([]);
  // console.log(data);
  // console.log(window.location.pathname);

  useEffect(() => {
    // fetch data
    const dataFetch = async () => {
      const data = await (
        await fetch(`http://localhost:8001/api/files/?` + new URLSearchParams({
            location: window.location.pathname || "/"
        }),
            {
                method: "GET",

                headers: new Headers({
                    Authorization: 'Token 17f914ca39030d6d0907f4d342c4627d1b17b038',
    }),
            }
        )
      ).json();

      // set state when the data received
      setData(data);
    };
    dataFetch();
  }, []);
  return (
    <div>
        <h1>Current Folder: {window.location.pathname}</h1>
      <h2>Found {data.length} File Versions</h2>
        <FileUpload></FileUpload>
      <div>
          <FileVersionsList file_versions={data} />
      </div>

    </div>
  );
}

export default FileVersions;
