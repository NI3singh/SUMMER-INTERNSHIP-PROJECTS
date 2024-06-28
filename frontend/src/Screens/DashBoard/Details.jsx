import SideBar from "./SideBar";

// Details component to display student profile information
function Details() {
  return (
    <SideBar>
      {/* Header for the student profile */}
      <div className="text-white font-bold text-3xl text-center border-4 border-b-2 border-white p-3">
        STUDENT PROFILE
      </div>
      {/* Content section for student details */}
      <div className="text-white font-semibold text-lg border-4 border-t-2 border-white">
        <div className="w-1/5 border-r-4 border-b-4 border-white p-4">
          Enrollment No.
        </div>
        <div className="w-1/5 border-r-4 border-b-4 border-white p-4">Name</div>
        <div className="w-1/5 border-r-4 border-white p-4">Division</div>
      </div>
    </SideBar>
  );
}

export default Details;
