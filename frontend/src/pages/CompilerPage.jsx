
import { useState } from "react"
import axios from "axios"

export default function CompilerPage() {

    const [prompt, setPrompt] = useState("")

    const [result, setResult] = useState(null)

    const [loading, setLoading] = useState(false)
    const [activeTab, setActiveTab] = useState("intent")

    async function generateApp() {

        try {

            setLoading(true)

            const response = await axios.post(
                "http://127.0.0.1:8000/compile-app",
                {
                    prompt: prompt
                }
            )

            setResult(response.data)

        } catch (error) {

            console.error(error)

        } finally {

            setLoading(false)

        }
    }

    return (

        <div className="min-h-screen bg-slate-950 text-white p-10">

            <h1
                className="
                    text-5xl
                    font-bold
                    mb-10
                    text-blue-400
                "
            >
                AI App Compiler
            </h1>

            <div
                className="
                    bg-slate-900
                    p-6
                    rounded-2xl
                    border
                    border-slate-800
                    mb-10
                "
            >

                <textarea
                    placeholder="
Build a CRM with login,
subscriptions and analytics...
                    "
                    value={prompt}
                    onChange={(e) =>
                        setPrompt(e.target.value)
                    }
                    className="
                        w-full
                        h-40
                        bg-slate-800
                        rounded-xl
                        p-4
                        outline-none
                        text-white
                    "
                />

                <button
                    onClick={generateApp}
                    className="
                        mt-6
                        bg-blue-500
                        hover:bg-blue-600
                        px-8
                        py-3
                        rounded-xl
                        font-semibold
                    "
                >

                    {
                        loading
                        ? "Generating..."
                        : "Generate App"
                    }

                </button>

            </div>

            {
                result && (

                   
<div>

    <div className="flex gap-4 mb-6 flex-wrap">

        <TabButton
            label="Intent"
            tab="intent"
            activeTab={activeTab}
            setActiveTab={setActiveTab}
        />

        <TabButton
            label="Architecture"
            tab="architecture"
            activeTab={activeTab}
            setActiveTab={setActiveTab}
        />

        <TabButton
            label="Database"
            tab="database"
            activeTab={activeTab}
            setActiveTab={setActiveTab}
        />

        <TabButton
            label="API"
            tab="api"
            activeTab={activeTab}
            setActiveTab={setActiveTab}
        />

        <TabButton
            label="UI"
            tab="ui"
            activeTab={activeTab}
            setActiveTab={setActiveTab}
        />

        <TabButton
            label="Models"
            tab="models"
            activeTab={activeTab}
            setActiveTab={setActiveTab}
        />

        <TabButton
            label="Routes"
            tab="routes"
            activeTab={activeTab}
            setActiveTab={setActiveTab}
        />

    </div>

    {
        activeTab === "intent" && (
            <Section
                title="Intent"
                data={result.intent}
            />
        )
    }

    {
        activeTab === "architecture" && (
            <Section
                title="Architecture"
                data={result.architecture}
            />
        )
    }

    {
        activeTab === "database" && (
            <Section
                title="Database Schema"
                data={result.database_schema}
            />
        )
    }

    {
        activeTab === "api" && (
            <Section
                title="API Schema"
                data={result.api_schema}
            />
        )
    }

    {
        activeTab === "ui" && (
            <Section
                title="UI Schema"
                data={result.ui_schema}
            />
        )
    }

    {
        activeTab === "models" && (
            <Section
                title="SQLAlchemy Models"
                data={result.sqlalchemy_models}
            />
        )
    }

    {
        activeTab === "routes" && (
            <Section
                title="FastAPI Routes"
                data={result.fastapi_routes}
            />
        )
    }

</div>




                   

                    
                )
            }

        </div>
    )
}


function Section({
    title,
    data
}) {

    return (

        <div
            className="
                bg-slate-900
                border
                border-slate-800
                rounded-2xl
                p-6
            "
        >

            <h2
                className="
                    text-2xl
                    font-bold
                    mb-4
                    text-blue-400
                "
            >
                {title}
            </h2>

            <pre
                className="
                    overflow-x-auto
                    text-sm
                    text-slate-300
                "
            >
                
{
    typeof data === "string"
    ? data
    : JSON.stringify(
        data,
        null,
        2
    )
}


            </pre>

        </div>
    )
}


function TabButton({
    label,
    tab,
    activeTab,
    setActiveTab
}) {

    return (

        <button
            onClick={() =>
                setActiveTab(tab)
            }
            className={`
                px-5
                py-2
                rounded-xl
                font-semibold
                transition

                ${
                    activeTab === tab
                    ? "bg-blue-500 text-white"
                    : "bg-slate-800 text-slate-300"
                }
            `}
        >
            {label}
        </button>
    )
}

