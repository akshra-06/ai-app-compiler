import { Link } from "react-router-dom";

export default function Sidebar() {
  return (
    <div
      className="
                w-64
                h-screen
                bg-slate-900
                border-r
                border-slate-800
                p-6
            "
    >
      <h1
        className="
                    text-3xl
                    font-bold
                    mb-10
                    text-blue-400
                "
      >
        CRM
      </h1>

      <div
        className="
                    flex
                    flex-col
                    gap-4
                "
      >
        <Link
          to="/contacts"
          className="
                        text-slate-300
                        hover:text-white
                    "
        >
          Contacts
        </Link>

        <Link
          to="/analytics"
          className="
                        text-slate-300
                        hover:text-white
                    "
        >
          Analytics
        </Link>

        <Link
          to="/subscriptions"
          className="
                        text-slate-300
                        hover:text-white
                    "
        >
          Subscriptions
        </Link>
      </div>
    </div>
  );
}
