import Layout from "../Layout/Layout";
import { Link } from "react-router-dom";
import { MdStart } from "react-icons/md";

function HomeScreen() {
  return (
    <Layout>
      <div className="flex flex-col justify-center items-center h-auto">
        <div className="container mx-auto min-h-auto px-2 bg-white">
          {/* Header */}
          <div className="font-medium text-8xl text-main text-center p-10">
            Welcome to Student Performance Analysis
          </div>
          {/* Start Button */}
          <div className="sm:col-span-1 col-span-1 flex justify-center font-bold text-sm p-5">
            <Link
              to="/role"
              className="bg-dry text-white hover:bg-subMain transitions rounded-xl flex-rows gap-5 w-fit sm:p-4 p-4"
            >
              <MdStart className="w-5 h-5" />
              Start
            </Link>
          </div>
        </div>
      </div>
    </Layout>
  );
}

export default HomeScreen;
