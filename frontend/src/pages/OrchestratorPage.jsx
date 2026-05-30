import { useState, useEffect, useRef } from "react";
import axios from "axios";
const API_URL = import.meta.env.VITE_API_URL;

function Card({ title, children }) {
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
                mb-6
                text-blue-400
            "
      >
        {title}
      </h2>

      {children}
    </div>
  );
}

function MetricCard({ label, value }) {
  return (
    <div
      className="
            bg-slate-800
            p-6
            rounded-xl
            text-center
        "
    >
      <h3 className="text-slate-400">{label}</h3>

      <p
        className="
                text-3xl
                font-bold
                mt-2
                text-blue-400
            "
      >
        {value}
      </p>
    </div>
  );
}

function PipelineStage({ title, active, completed }) {
  return (
    <div
      className="
            flex
            items-center
            justify-between
            bg-slate-800
            p-4
            rounded-xl
        "
    >
      <h3 className="font-semibold">{title}</h3>

      <div>
        {active && !completed && (
          <span
            className="
                            text-yellow-400
                            animate-pulse
                        "
          >
            ⏳ Running
          </span>
        )}

        {completed && (
          <span
            className="
                            text-green-400
                        "
          >
            ✓ Completed
          </span>
        )}
      </div>
    </div>
  );
}

export default function OrchestratorPage() {
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [activeStage, setActiveStage] = useState("");
  const [prompt, setPrompt] = useState("");

  const [copied, setCopied] = useState("");
  const eventSourceRef = useRef(null);

  const timeoutRef = useRef(null);
  const [completedStages, setCompletedStages] = useState([]);
  const [selectedModel, setSelectedModel] = useState("auto");
  useEffect(() => {
    return () => {
      eventSourceRef.current?.close();
      if (timeoutRef.current) {
        clearTimeout(timeoutRef.current);
      }
    };
  }, []);

  function copySQLAlchemy() {
    if (result?.sqlalchemy_models) {
      navigator.clipboard.writeText(result.sqlalchemy_models);
    }

    setCopied("sql");

    timeoutRef.current = setTimeout(() => {
      setCopied("");
    }, 2000);
  }

  function copyFastAPI() {
    if (result?.fastapi_routes) {
      navigator.clipboard.writeText(result.fastapi_routes);
    }
    setCopied("fastapi");

    timeoutRef.current = setTimeout(() => {
      setCopied("");
    }, 2000);
  }

  function copyReact() {
    if (result?.react_pages) {
      navigator.clipboard.writeText(
        JSON.stringify(result.react_pages, null, 2),
      );
    }
    setCopied("react");

    timeoutRef.current = setTimeout(() => {
      setCopied("");
    }, 2000);
  }

async function testIntegration(integrationId) {
  try {
    const response = await axios.post(
      `${API_URL}/test-integration/${integrationId}`
    );

    console.log(response.data);

    alert(
      response.data.message ||
      `${integrationId} integration test successful`
    );
  } catch (error) {
    console.error(error);

    alert(
      error.response?.data?.detail ||
      "Integration test failed"
    );
  }
}

  async function runPipeline() {
    console.log("RUN PIPELINE STARTED");
    setCompletedStages([]);
    setActiveStage("");
    if (loading) return;
    if (!prompt.trim()) {
      alert("Please enter a prompt");
      return;
    }
    try {
      setLoading(true);

      setResult(null);

      if (eventSourceRef.current) {
        eventSourceRef.current.close();
      }
      eventSourceRef.current = new EventSource(
        `${API_URL}/stream-generate`,
      );

      const eventSource = eventSourceRef.current;
      eventSource.onmessage = (event) => {
        console.log("RAW SSE:", event.data);

        const data = JSON.parse(event.data);

        console.log("PARSED SSE:", data);

        if (data.event === "stage_start") {
          setActiveStage(data.stage);
        }

        if (data.event === "stage_complete") {
          setCompletedStages((prev) =>
            prev.includes(data.stage) ? prev : [...prev, data.stage],
          );

          setActiveStage("");
        }

        if (data.event === "generation_complete") {
          eventSource.close();
        }
      };
      eventSource.onerror = (error) => {
        console.error("SSE Error:", error);
        eventSource.close();
      };

      const response = await axios.post(
         `${API_URL}/orchestrate-real`,

        {
  prompt: prompt,
  model: selectedModel
},
      );
      console.log(
  "ORCHESTRATE RESPONSE",
  response.data
);

      setResult(response.data);
      console.log("RESULT STATE:", response.data);
    } catch (error) {
      console.error(error);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="min-h-screen bg-slate-950 text-white p-10">
      <h1 className="text-5xl font-bold text-blue-400 mb-8">
        AI Orchestration Dashboard
      </h1>
      <div
        className="
    bg-slate-900
    border
    border-slate-800
    rounded-2xl
    p-6
    mb-8
"
      >
        <h2
          className="
        text-2xl
        font-bold
        text-blue-400
        mb-4
    "
        >
          Prompt Input
        </h2>

        <textarea
          value={prompt}
          onChange={(e) => setPrompt(e.target.value)}
          placeholder="
Build a CRM with:
- authentication
- Slack notifications
- analytics dashboard
"
          className="
            w-full
            h-40
            bg-slate-800
            border
            border-slate-700
            rounded-xl
            p-4
            text-white
            outline-none
        "
        />

<div className="mb-4">
  <label className="block mb-2 text-sm font-medium">
  Select Model
</label>

<select
  value={selectedModel}
  onChange={(e) => setSelectedModel(e.target.value)}
  className="
    bg-slate-800
    border
    border-slate-700
    rounded-lg
    px-4
    py-2
    w-full
  "
>
  <option value="auto">
    Auto (Recommended)
  </option>

  <option value="openai/gpt-3.5-turbo">
    GPT-3.5 Turbo
  </option>

  <option value="openai/gpt-4o-mini">
    GPT-4o Mini
  </option>

  <option value="openai/gpt-4o">
    GPT-4o
  </option>


  <option value="google/gemini-2.0-flash-lite-001">
    Gemini 1.5 Pro
  </option>

</select>
</div>
        <button
          onClick={runPipeline}
          className="
            mt-4
            bg-blue-500
            hover:bg-blue-600
            px-6
            py-3
            rounded-xl
            font-semibold
        "
          disabled={loading}
        >
          Generate App
        </button>
      </div>
     
      {(loading || result) && (
        <div
          className="
            mb-10
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
                mb-6
                text-blue-400
            "
          >
            Pipeline Execution
          </h2>
          <div className="text-red-400 mb-4">
            Active Stage: {activeStage || "NONE"}
          </div>
          <div className="space-y-4">
            <PipelineStage
              title="Intent Extraction"
              active={activeStage === "intent_extraction"}
              completed={completedStages.includes("intent_extraction")}
            />

            <PipelineStage
              title="Architecture Generation"
              active={activeStage === "schema_generation"}
              completed={completedStages.includes("schema_generation")}
            />

            <PipelineStage
              title="Database Generation"
              active={activeStage === "appspec_generation"}
              completed={completedStages.includes("appspec_generation")}
            />

            <PipelineStage
              title="API/UI Generation"
              active={activeStage === "validation"}
              completed={completedStages.includes("validation")}
            />

            <PipelineStage
              title="Repair"
              active={activeStage === "repair"}
              completed={completedStages.includes("repair")}
            />
          </div>
        </div>
      )}
    
      {result && (
        <div className="space-y-8">
          <Card title="Generation Summary">
            <div
              className="
    mb-6
    bg-green-500/10
    border
    border-green-500/30
    text-green-400
    p-4
    rounded-xl
    font-semibold
  "
            >
              ✅ Application Generated Successfully
            </div>
            <div className="grid grid-cols-2 md:grid-cols-5 gap-4">
              <div className="bg-slate-800 p-4 rounded-xl text-center">
                <div className="text-sm text-slate-400">Application</div>

                <div className="text-xl font-bold text-blue-400">
                  {result.intent?.app_name || "N/A"}
                </div>
              </div>

              <div className="bg-slate-800 p-4 rounded-xl text-center">
                <div className="text-sm text-slate-400">Entities</div>

                <div className="text-xl font-bold text-green-400">
                  {result.architecture?.entities?.length || 0}
                </div>
              </div>

              <div className="bg-slate-800 p-4 rounded-xl text-center">
                <div className="text-sm text-slate-400">Tables</div>

                <div className="text-xl font-bold text-yellow-400">
                  {result.database_schema?.tables?.length || 0}
                </div>
              </div>

              <div className="bg-slate-800 p-4 rounded-xl text-center">
                <div className="text-sm text-slate-400">APIs</div>

                <div className="text-xl font-bold text-purple-400">
                  {result.api_schema?.endpoints?.length || 0}
                </div>
              </div>

              <div className="bg-slate-800 p-4 rounded-xl text-center">
                <div className="text-sm text-slate-400">Pages</div>

                <div className="text-xl font-bold text-pink-400">
                  {result.ui_schema?.pages?.length || 0}
                </div>
              </div>
            </div>

            <div className="bg-slate-800 p-4 rounded-xl text-center">
  <div className="text-sm text-slate-400">
    Model
  </div>

  <div className="text-xl font-bold text-cyan-400">
    {selectedModel}
  </div>
</div>
          </Card>
          <Card title="Intent">
            <div className="space-y-6">
              <div>
                <h3 className="text-lg font-semibold text-slate-300">
                  App Name
                </h3>

                <p className="text-2xl font-bold text-blue-400">
                  {result.intent?.app_name}
                </p>
              </div>

              <div>
                <h3 className="text-lg font-semibold text-slate-300 mb-2">
                  Features
                </h3>

                <ul className="space-y-2">
                  {result.intent?.features?.map((feature, index) => (
                    <li
                      key={index}
                      className="
                bg-slate-800
                p-3
                rounded-lg
              "
                    >
                      • {feature}
                    </li>
                  ))}
                </ul>
              </div>

              <div>
                <h3 className="text-lg font-semibold text-slate-300 mb-2">
                  Roles
                </h3>

                <div className="flex gap-2 flex-wrap">
                  {result.intent?.roles?.map((role, index) => (
                    <span
                      key={index}
                      className="
                bg-blue-500/20
                text-blue-400
                px-3
                py-1
                rounded-full
              "
                    >
                      {role}
                    </span>
                  ))}
                </div>
              </div>

              <div>
                <h3 className="text-lg font-semibold text-slate-300 mb-2">
                  Entities
                </h3>

                <div className="flex gap-2 flex-wrap">
                  {result.intent?.entities?.map((entity, index) => (
                    <span
                      key={index}
                      className="
                bg-green-500/20
                text-green-400
                px-3
                py-1
                rounded-full
              "
                    >
                      {entity}
                    </span>
                  ))}
                </div>
              </div>
            </div>
          </Card>

          <Card title="Architecture">
            <div className="grid md:grid-cols-2 gap-4">
              {result.architecture?.entities?.map((entity, index) => (
                <div
                  key={index}
                  className="
          bg-slate-800
          p-4
          rounded-xl
        "
                >
                  <h3 className="font-bold text-green-400 mb-3">
                    {entity.name}
                  </h3>

                  <div className="space-y-2">
                    {entity.fields?.map((field, idx) => (
                      <div
                        key={idx}
                        className="
                bg-slate-700
                px-3
                py-2
                rounded-lg
              "
                      >
                        {field.name}
                        <span className="text-slate-400 ml-2">
                          ({field.type})
                        </span>
                      </div>
                    ))}
                  </div>
                </div>
              ))}
            </div>
          </Card>

          <Card title="Database Schema">
            <div className="space-y-4">
              {result.database_schema?.tables?.map((table, index) => (
                <div
                  key={index}
                  className="
          bg-slate-800
          p-4
          rounded-xl
        "
                >
                  <h3 className="font-bold text-yellow-400 mb-3">
                    {table.name}
                  </h3>

                  <ul className="space-y-2">
                    {table.columns?.map((column, idx) => (
                      <li key={idx}>
                        {column.name}
                        <span className="text-slate-400 ml-2">
                          ({column.type})
                        </span>
                      </li>
                    ))}
                  </ul>
                </div>
              ))}
            </div>
          </Card>

          <Card title="API Schema">
            <div className="space-y-3">
              {result.api_schema?.endpoints?.map((endpoint, index) => (
                <div
                  key={index}
                  className="
          bg-slate-800
          p-3
          rounded-xl
          flex
          justify-between
        "
                >
                  <span className="font-bold text-blue-400">
                    {endpoint.method}
                  </span>

                  <span>{endpoint.path}</span>
                </div>
              ))}
            </div>
          </Card>

          <Card title="UI Schema">
            <div className="grid md:grid-cols-2 gap-4">
              {result.ui_schema?.pages?.map((page, index) => (
                <div
                  key={index}
                  className="
          bg-slate-800
          p-4
          rounded-xl
        "
                >
                  <h3 className="font-bold text-purple-400">{page.name}</h3>

                  <p className="text-slate-400">{page.route}</p>

                  <div className="mt-3 space-y-2">
                    {page.components?.map((component, idx) => (
                      <div
                        key={idx}
                        className="
                bg-slate-700
                px-3
                py-2
                rounded-lg
              "
                      >
                        {component.name}
                      </div>
                    ))}
                  </div>
                </div>
              ))}
            </div>
          </Card>

          <Card title="Supported Integrations">
            <div className="grid md:grid-cols-5 gap-4">
              <div className="bg-slate-800 p-4 rounded-xl text-center">
                <div className="text-2xl mb-2">💬</div>

                <div className="font-semibold text-blue-400">Slack</div>

                <div className="text-xs text-slate-400 mt-2">send_message</div>

                <button
                  onClick={() => testIntegration("slack")}
                  className="
            mt-4
            bg-blue-500
            hover:bg-blue-600
            px-4
            py-2
            rounded-lg
            cursor-pointer
        "
                >
                  Test Integration
                </button>
              </div>

              <div className="bg-slate-800 p-4 rounded-xl text-center">
                <div className="text-2xl mb-2">📧</div>

                <div className="font-semibold text-red-400">Gmail</div>

                <div className="text-xs text-slate-400 mt-2">send_email</div>

                <button
                  onClick={() => testIntegration("gmail")}
                  className="
            mt-4
            bg-blue-500
            hover:bg-blue-600
            px-4
            py-2
            rounded-lg
            cursor-pointer
        "
                >
                  Test Integration
                </button>
              </div>

              <div className="bg-slate-800 p-4 rounded-xl text-center">
                <div className="text-2xl mb-2">💳</div>

                <div className="font-semibold text-green-400">Stripe</div>

                <div className="text-xs text-slate-400 mt-2">
                  create_customer
                </div>

                <button
                  onClick={() => testIntegration("stripe")}
                  className="
            mt-4
            bg-blue-500
            hover:bg-blue-600
            px-4
            py-2
            rounded-lg
            cursor-pointer
        "
                >
                  Test Integration
                </button>
              </div>

              <div className="bg-slate-800 p-4 rounded-xl text-center">
                <div className="text-2xl mb-2">📱</div>

                <div className="font-semibold text-emerald-400">WhatsApp</div>

                <div className="text-xs text-slate-400 mt-2">
                  send_template_message
                </div>

                <button
                  onClick={() => testIntegration("whatsapp")}
                  className="
            mt-4
            bg-blue-500
            hover:bg-blue-600
            px-4
            py-2
            rounded-lg
            cursor-pointer
        "
                >
                  Test Integration
                </button>
              </div>

              <div className="bg-slate-800 p-4 rounded-xl text-center">
                <div className="text-2xl mb-2">🔗</div>

                <div className="font-semibold text-purple-400">Webhook</div>

                <div className="text-xs text-slate-400 mt-2">post_payload</div>

                <button
                  onClick={() => testIntegration("webhook")}
                  className="
            mt-4
            bg-blue-500
            hover:bg-blue-600
            px-4
            py-2
            rounded-lg
            cursor-pointer
        "
                >
                  Test Integration
                </button>
              </div>
            </div>
          </Card>
          <button
            onClick={copySQLAlchemy}
            className="
    bg-blue-500
    hover:bg-blue-600
    px-4
    py-2
    rounded-lg
    cursor-pointer
    transition
    hover:scale-105
active:scale-95
duration-200
  "
          >
            {copied === "sql" ? "✅ Copied!" : "📋 Copy"}
          </button>
          <Card title="Generated Code">
            <div className="space-y-6">
              <div>
                <h3 className="text-lg font-semibold text-green-400 mb-2">
                  SQLAlchemy Models
                </h3>

                <pre
                  className="
    bg-slate-900
    p-4
    rounded-xl
    overflow-x-auto
    whitespace-pre-wrap
  "
                >
                  {result.sqlalchemy_models}
                </pre>
              </div>
              <button
                onClick={copyFastAPI}
                className="
    bg-blue-500
    hover:bg-blue-600
    px-4
    py-2
    rounded-lg
    cursor-pointer
    transition
    hover:scale-105
active:scale-95
duration-200
  "
              >
                {copied === "fastapi" ? "✅ Copied!" : "📋 Copy"}
              </button>
              <div>
                <h3 className="text-lg font-semibold text-blue-400 mb-2">
                  FastAPI Routes
                </h3>

                <pre
                  className="
    bg-slate-900
    p-4
    rounded-xl
    overflow-x-auto
    whitespace-pre-wrap
  "
                >
                  {result.fastapi_routes}
                </pre>
              </div>
              <button
                onClick={copyReact}
                className="
    bg-blue-500
    hover:bg-blue-600
    px-4
    py-2
    rounded-lg
    cursor-pointer
    transition
    hover:scale-105
active:scale-95
duration-200
  "
              >
                {copied === "react" ? "✅ Copied!" : "📋 Copy"}
              </button>
              <div>
                <h3 className="text-lg font-semibold text-purple-400 mb-2">
                  React Pages
                </h3>

                <pre
                  className="
    bg-slate-900
    p-4
    rounded-xl
    overflow-x-auto
    text-sm
    whitespace-pre-wrap
  "
                >
                  {JSON.stringify(result.react_pages, null, 2)}
                </pre>
              </div>
            </div>
                  </Card>
        </div>
      )}
    </div>
  );
}
