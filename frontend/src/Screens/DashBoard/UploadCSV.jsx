import { useRef, useState } from "react";
import SideBar from "./SideBar";
import { FaUpload } from "react-icons/fa";
import axios from "axios";

function UploadCSV() {
  // State variables to store the selected files
  const [trainFile, setTrainFile] = useState(null);
  const [testFile, setTestFile] = useState(null);
  const [rawFile, setRawFile] = useState(null);

  // References to file input elements
  const trainFileInputRef = useRef(null);
  const testFileInputRef = useRef(null);
  const rawFileInputRef = useRef(null);

  // Handlers for file input changes
  function handleTrainChange(event) {
    setTrainFile(event.target.files[0]);
  }

  function handleTestChange(event) {
    setTestFile(event.target.files[0]);
  }

  function handleRawChange(event) {
    setRawFile(event.target.files[0]);
  }

  // Handler for form submission to upload the raw file
  function handleRawSubmit(event) {
    event.preventDefault();
    const url = "https://student-performance-analysis-7du3.onrender.com/upload";
    const formData = new FormData();
    formData.append("file", rawFile);
    const config = {
      headers: {
        "content-type": "multipart/form-data",
      },
    };
    axios
      .post(url, formData, config)
      .then((response) => {
        console.log(response.data);
      })
      .catch((error) => {
        console.error("Error uploading file:", error);
      });
  }

  return (
    <SideBar>
      <form onSubmit={handleRawSubmit}>
        <div className="text-white font-bold text-center p-5 border-4 border-b-2 border-white">
          Upload Train and Test Separately
        </div>
        <div className="border-4 border-y-2 border-white">
          <div className="grid sm:grid-cols-2 lg:grid-cols-2 gap-6 m-4 justify-center">
            <div className="flex justify-center">
              <input
                type="file"
                ref={trainFileInputRef}
                onChange={handleTrainChange}
                style={{ display: "none" }}
              />
              <button
                type="button"
                onClick={() => trainFileInputRef.current.click()}
                className="bg-dry text-white hover:bg-subMain transitions rounded-xl flex-rows gap-5 w-4/5 sm:p-4 p-4 justify-center"
              >
                <FaUpload /> {trainFile ? trainFile.name : "Train Data"}
              </button>
            </div>
            <div className="flex justify-center">
              <input
                type="file"
                ref={testFileInputRef}
                onChange={handleTestChange}
                style={{ display: "none" }}
              />
              <button
                type="button"
                onClick={() => testFileInputRef.current.click()}
                className="bg-dry text-white hover:bg-subMain transitions rounded-xl flex-rows gap-5 w-4/5 sm:p-4 p-4 justify-center"
              >
                <FaUpload /> {testFile ? testFile.name : "Test Data"}
              </button>
            </div>
          </div>
        </div>
        <div className="text-white font-bold text-center p-5 border-4 border-y-2 border-white">
          Or
        </div>
        <div className="text-white font-bold text-center p-5 border-4 border-y-2 border-white">
          Upload Whole Data
        </div>
        <div className="border-4 border-y-2 border-white">
          <div className="gap-6 m-4 justify-center p-5">
            <div className="flex justify-center">
              <input
                type="file"
                ref={rawFileInputRef}
                onChange={handleRawChange}
                style={{ display: "none" }}
              />
              <button
                type="button"
                onClick={() => rawFileInputRef.current.click()}
                className="bg-dry text-white hover:bg-subMain transitions rounded-xl flex-rows gap-5 w-4/5 sm:p-4 p-4 justify-center"
              >
                <FaUpload /> {rawFile ? rawFile.name : "Raw Data"}
              </button>
            </div>
          </div>
        </div>
        <div className="border-4 border-y-2 border-white">
          <div className="flex justify-center p-5">
            <button
              type="submit"
              className="bg-star text-white hover:bg-subMain transitions rounded-xl flex-rows gap-5 w-2/5 sm:p-4 p-4"
            >
              Submit
            </button>
          </div>
        </div>
      </form>
    </SideBar>
  );
}

export default UploadCSV;
