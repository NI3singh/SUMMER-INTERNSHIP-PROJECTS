import { FaDownload } from "react-icons/fa";
import SideBar from "./SideBar";
import axios from "axios";
import FileDownload from "js-file-download";

// Download component for downloading an Excel file from the server
function Download() {
  // Function to handle the download request
  function download(event) {
    event.preventDefault();
    const url = "http://127.0.0.1:5000/download_data";
    const config = {
      responseType: "blob", // Set response type to blob for file download
    };

    // Axios GET request to download the file
    axios
      .get(url, config)
      .then((res) => {
        FileDownload(res.data, "Data.xlsx");
      })
      .catch((err) => console.error(err));
  }

  return (
    <SideBar>
      {/* Header for the download section */}
      <div className="text-white font-bold text-center p-5 border-4 border-b-2 border-white">
        Download Excel File
      </div>
      <div className="border-4 border-y-2 border-white">
        <div className="gap-6 m-4 justify-center p-5">
          <div className="flex justify-center">
            {/* Download button */}
            <button
              type="submit"
              className="bg-dry text-white hover:bg-subMain transitions rounded-xl flex-rows gap-5 w-2/5 sm:p-4 p-4 justify-center"
              onClick={download}
            >
              <FaDownload /> Download Excel File
            </button>
          </div>
        </div>
      </div>
    </SideBar>
  );
}

export default Download;
