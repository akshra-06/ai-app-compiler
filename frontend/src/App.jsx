
import {
    BrowserRouter,
    Routes,
    Route,
    Navigate
} from "react-router-dom"

// import AnalyticsPage from "./pages/AnalyticsPage"
// import LoginPage from "./pages/LoginPage"
// import ContactsPage from "./pages/ContactsPage"

import OrchestratorPage from "./pages/OrchestratorPage"


function App() {

    return (

        <BrowserRouter>

            <Routes>

                {/* <Route
                    path="/"
                    element={<Navigate to="/login" />}
                />

                <Route
                    path="/login"
                    element={<LoginPage />}
                />

                <Route
                    path="/contacts"
                    element={<ContactsPage />}
                />

                <Route
                    path="/analytics"
                    element={<AnalyticsPage />}
                /> */}

                <Route
                    path="/orchestrator"
                    element={<OrchestratorPage />}
                />

            </Routes>

        </BrowserRouter>
    )
}

export default App

