import { Link } from "react-router-dom";
import Layout from "../Layout/Layout";

function Role() {
  return (
    <Layout>
      <div className="container mx-auto px-2 my-24 flex-colo">
        <div className="w-auto 2xl:w-1/5 gap-8 flex-colo p-6 sm:p-10 md:w-2/5 bg-main rounded-lg border border-border">
          <img
            src="site-logo-white-2.png"
            alt="logo"
            className="w-auto h-10 object-contain"
          />
          <div className="text-white">Select Your Role</div>
          <div className="w-full">
            <Link
              to="/upload_csv"
              className="bg-dry text-white hover:bg-subMain transtions rounded-xl flex-rows gap-5 w-full sm:p-4 p-4"
            >
              Student
            </Link>
          </div>
          <div className="w-full">
            <Link
              to="/teacher_dashboard"
              className="bg-dry text-white hover:bg-subMain transtions rounded-xl flex-rows gap-5 w-full sm:p-4 p-4"
            >
              Teacher
            </Link>
          </div>
          <div className="w-full">
            <Link
              to="/admin_dashboard"
              className="bg-dry text-white hover:bg-subMain transtions rounded-xl flex-rows gap-5 w-full sm:p-4 p-4"
            >
              Admin
            </Link>
          </div>
        </div>
      </div>
    </Layout>
  );
}

export default Role;
