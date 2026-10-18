import React, { useState, useEffect, useCallback, useMemo } from "react";
import ReactFlow, {
  addEdge,
  Background,
  Controls,
  MiniMap,
  useNodesState,
  useEdgesState,
  MarkerType,
} from "reactflow";
import {
  Play,
  PlusCircle,
  Sparkles,
  RotateCcw,
  Layers,
  Activity,
  Terminal,
  Settings,
  HelpCircle
} from "lucide-react";

import { Button } from "./components/ui/button";
import { Input } from "./components/ui/input";
import { Badge } from "./components/ui/badge";
import { Card, CardHeader, CardTitle, CardContent } from "./components/ui/card";
import { StartNode, DecisionNode, OutcomeNode } from "./components/CustomNodes";
import { YesNoEdge } from "./components/YesNoEdge";

const API_BASE = "http://127.0.0.1:8000";

// Default fallback flow if backend is offline or loading
const INITIAL_NODES = [
  {
    id: "start",
    type: "start",
    position: { x: 300, y: 30 },
    data: { label: "Incoming User Ticket" },
  },
  {
    id: "dec-1",
    type: "decision",
    position: { x: 270, y: 150 },
    data: {
      label: "Is Critical Priority?",
      prompt: "Does this ticket describe complete system downtime, outage, or security breach?",
    },
  },
  {
    id: "out-p1",
    type: "outcome",
    position: { x: 100, y: 360 },
    data: { label: "Page On-Call DevOps Team" },
  },
  {
    id: "dec-2",
    type: "decision",
    position: { x: 440, y: 340 },
    data: {
      label: "Billing Issue?",
      prompt: "Is the user requesting a refund, invoice correction, or billing inquiry?",
    },
  },
  {
    id: "out-billing",
    type: "outcome",
    position: { x: 340, y: 540 },
    data: { label: "Route to Finance Ops" },
  },
  {
    id: "out-standard",
    type: "outcome",
    position: { x: 580, y: 540 },
    data: { label: "Auto-Reply with FAQ" },
  },
];

const INITIAL_EDGES = [
  {
    id: "e-start-dec1",
    source: "start",
    target: "dec-1",
    type: "yesNoEdge",
    data: { branch: "DEFAULT" },
    markerEnd: { type: MarkerType.ArrowClosed },
  },
  {
    id: "e-dec1-yes",
    source: "dec-1",
    sourceHandle: "YES",
    target: "out-p1",
    type: "yesNoEdge",
    data: { branch: "YES" },
    markerEnd: { type: MarkerType.ArrowClosed },
  },
  {
    id: "e-dec1-no",
    source: "dec-1",
    sourceHandle: "NO",
    target: "dec-2",
    type: "yesNoEdge",
    data: { branch: "NO" },
    markerEnd: { type: MarkerType.ArrowClosed },
  },
  {
    id: "e-dec2-yes",
    source: "dec-2",
    sourceHandle: "YES",
    target: "out-billing",
    type: "yesNoEdge",
    data: { branch: "YES" },
    markerEnd: { type: MarkerType.ArrowClosed },
  },
  {
    id: "e-dec2-no",
    source: "dec-2",
    sourceHandle: "NO",
    target: "out-standard",
    type: "yesNoEdge",
    data: { branch: "NO" },
    markerEnd: { type: MarkerType.ArrowClosed },
  },
];

export default function App() {
  const [nodes, setNodes, onNodesChange] = useNodesState(INITIAL_NODES);
  const [edges, setEdges, onEdgesChange] = useEdgesState(INITIAL_EDGES);
  const [selectedNode, setSelectedNode] = useState(null);
  const [inputContext, setInputContext] = useState(
    "Production database cluster is unreachable. Users receiving 504 gateway timeout on login since 10 minutes."
  );
  const [sampleFlows, setSampleFlows] = useState({});
  const [activeFlowId, setActiveFlowId] = useState("support_ticket_triage");
  const [isRunning, setIsRunning] = useState(false);
  const [executionResult, setExecutionResult] = useState(null);
  const [backendStatus, setBackendStatus] = useState("checking");

  const nodeTypes = useMemo(
    () => ({
      start: StartNode,
      decision: DecisionNode,
      outcome: OutcomeNode,
    }),
    []
  );

  const edgeTypes = useMemo(
    () => ({
      yesNoEdge: YesNoEdge,
    }),
    []
  );

  // Check backend health & fetch sample flows
  useEffect(() => {
    fetch(`${API_BASE}/health`)
      .then((res) => res.json())
      .then((data) => {
        setBackendStatus("connected");
      })
      .catch(() => {
        setBackendStatus("offline");
      });

    fetch(`${API_BASE}/api/sample-flows`)
      .then((res) => res.json())
      .then((flows) => {
        setSampleFlows(flows);
      })
      .catch(() => {});
  }, []);

  const onConnect = useCallback(
    (params) => {
      const branchType = params.sourceHandle === "YES" ? "YES" : params.sourceHandle === "NO" ? "NO" : "DEFAULT";
      const newEdge = {
        ...params,
        type: "yesNoEdge",
        data: { branch: branchType },
        markerEnd: { type: MarkerType.ArrowClosed },
      };
      setEdges((eds) => addEdge(newEdge, eds));
    },
    [setEdges]
  );

  const onNodeClick = useCallback((event, node) => {
    setSelectedNode(node);
  }, []);

  const handleUpdateSelectedNode = (field, value) => {
    if (!selectedNode) return;
    setNodes((nds) =>
      nds.map((node) => {
        if (node.id === selectedNode.id) {
          const updated = {
            ...node,
            data: {
              ...node.data,
              [field]: value,
            },
          };
          setSelectedNode(updated);
          return updated;
        }
        return node;
      })
    );
  };

  const handleAddDecisionNode = () => {
    const newId = `dec-${Date.now().toString().slice(-4)}`;
    const newNode = {
      id: newId,
      type: "decision",
      position: { x: 300 + Math.random() * 80, y: 250 + Math.random() * 80 },
      data: {
        label: "New AI Decision",
        prompt: "Analyze context and evaluate if requirement is satisfied.",
      },
    };
    setNodes((nds) => [...nds, newNode]);
  };

  const handleAddOutcomeNode = () => {
    const newId = `out-${Date.now().toString().slice(-4)}`;
    const newNode = {
      id: newId,
      type: "outcome",
      position: { x: 300 + Math.random() * 80, y: 450 + Math.random() * 80 },
      data: {
        label: "Custom Action",
      },
    };
    setNodes((nds) => [...nds, newNode]);
  };

  const handleSelectSampleFlow = (flowKey) => {
    setActiveFlowId(flowKey);
    const flow = sampleFlows[flowKey];
    if (!flow) return;

    const formattedNodes = flow.nodes.map((n) => ({
      id: n.id,
      type: n.type,
      position: { x: n.x || 200, y: n.y || 100 },
      data: {
        label: n.label,
        prompt: n.prompt,
      },
    }));

    const formattedEdges = flow.edges.map((e) => ({
      id: e.id,
      source: e.source,
      sourceHandle: e.branch,
      target: e.target,
      type: "yesNoEdge",
      data: { branch: e.branch },
      markerEnd: { type: MarkerType.ArrowClosed },
    }));

    setNodes(formattedNodes);
    setEdges(formattedEdges);
    setExecutionResult(null);
  };

  const handleRunFlow = async () => {
    setIsRunning(true);
    setExecutionResult(null);

    // Reset previous execution highlights
    setNodes((nds) =>
      nds.map((n) => ({
        ...n,
        data: { ...n.data, isActive: false, decisionResult: null },
      }))
    );
    setEdges((eds) =>
      eds.map((e) => ({
        ...e,
        data: { ...e.data, isActive: false },
      }))
    );

    const payload = {
      graph: {
        id: activeFlowId,
        name: "Decision Flow",
        nodes: nodes.map((n) => ({
          id: n.id,
          label: n.data.label || "",
          type: n.type,
          prompt: n.data.prompt || null,
          x: n.position.x,
          y: n.position.y,
        })),
        edges: edges.map((e) => ({
          id: e.id,
          source: e.source,
          target: e.target,
          branch: e.data?.branch || "DEFAULT",
        })),
      },
      input_context: inputContext,
    };

    try {
      const response = await fetch(`${API_BASE}/api/run`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });

      const result = await response.json();
      setExecutionResult(result);

      if (result.trace) {
        // Highlight active nodes & decisions
        const activeNodeIds = new Set(result.trace.map((t) => t.node_id));
        const decisionMap = {};
        result.trace.forEach((t) => {
          if (t.decision) decisionMap[t.node_id] = t.decision;
        });

        setNodes((nds) =>
          nds.map((n) => ({
            ...n,
            data: {
              ...n.data,
              isActive: activeNodeIds.has(n.id),
              decisionResult: decisionMap[n.id] || null,
            },
          }))
        );

        // Highlight traversed edges
        const traversedEdges = new Set();
        for (let i = 0; i < result.trace.length - 1; i++) {
          const fromNode = result.trace[i].node_id;
          const toNode = result.trace[i + 1].node_id;
          traversedEdges.add(`${fromNode}->${toNode}`);
        }

        setEdges((eds) =>
          eds.map((e) => {
            const edgeKey = `${e.source}->${e.target}`;
            return {
              ...e,
              data: {
                ...e.data,
                isActive: traversedEdges.has(edgeKey),
              },
            };
          })
        );
      }
    } catch (err) {
      console.error("Execution error:", err);
      alert("Failed to execute flow against backend: " + err.message);
    } finally {
      setIsRunning(false);
    }
  };

  return (
    <div className="flex h-screen w-screen flex-col overflow-hidden bg-slate-50">
      {/* Header Bar */}
      <header className="flex h-14 items-center justify-between border-b border-slate-200 bg-white px-6 shadow-sm">
        <div className="flex items-center gap-3">
          <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-indigo-600 text-white shadow">
            <Sparkles size={18} />
          </div>
          <div>
            <h1 className="text-sm font-bold text-slate-900 leading-tight">
              AI Decision Flow Studio
            </h1>
            <p className="text-[11px] text-slate-500">
              React Flow Visual Canvas &bull; Inngest Multi-Step Orchestrator
            </p>
          </div>
          <Badge
            variant={backendStatus === "connected" ? "success" : "destructive"}
            className="ml-2 text-[10px]"
          >
            Backend: {backendStatus}
          </Badge>
        </div>

        {/* Toolbar Controls */}
        <div className="flex items-center gap-2">
          {Object.keys(sampleFlows).length > 0 && (
            <select
              value={activeFlowId}
              onChange={(e) => handleSelectSampleFlow(e.target.value)}
              className="h-8 rounded-md border border-slate-300 bg-white px-2.5 text-xs text-slate-700 shadow-sm focus:outline-none"
            >
              {Object.entries(sampleFlows).map(([key, f]) => (
                <option key={key} value={key}>
                  {f.name}
                </option>
              ))}
            </select>
          )}

          <Button
            variant="outline"
            size="sm"
            onClick={handleAddDecisionNode}
            className="gap-1.5"
          >
            <PlusCircle size={14} className="text-indigo-600" />
            + Decision Node
          </Button>

          <Button
            variant="outline"
            size="sm"
            onClick={handleAddOutcomeNode}
            className="gap-1.5"
          >
            <PlusCircle size={14} className="text-emerald-600" />
            + Outcome Node
          </Button>

          <Button
            variant="default"
            size="sm"
            onClick={handleRunFlow}
            disabled={isRunning}
            className="gap-1.5 bg-indigo-600 hover:bg-indigo-700 text-white shadow"
          >
            <Play size={14} className={isRunning ? "animate-spin" : ""} />
            {isRunning ? "Executing Inngest Flow..." : "Run Flow"}
          </Button>
        </div>
      </header>

      {/* Main Workspace Layout */}
      <div className="flex flex-1 overflow-hidden">
        {/* Left / Center Canvas Area */}
        <div className="flex-1 relative h-full">
          <ReactFlow
            nodes={nodes}
            edges={edges}
            onNodesChange={onNodesChange}
            onEdgesChange={onEdgesChange}
            onConnect={onConnect}
            onNodeClick={onNodeClick}
            nodeTypes={nodeTypes}
            edgeTypes={edgeTypes}
            fitView
            className="bg-slate-100"
          >
            <Background gap={16} size={1} color="#CBD5E1" />
            <Controls className="bg-white border border-slate-200 rounded shadow-sm" />
            <MiniMap
              nodeStrokeColor="#64748B"
              nodeColor={(n) => {
                if (n.type === "decision") return "#3B82F6";
                if (n.type === "outcome") return "#10B981";
                return "#6366F1";
              }}
              className="border border-slate-200 rounded-lg shadow-sm"
            />
          </ReactFlow>
        </div>

        {/* Right Inspector & Run Console Panel */}
        <div className="w-96 border-l border-slate-200 bg-white flex flex-col h-full shadow-lg z-10">
          <div className="p-4 border-b border-slate-200 flex items-center justify-between bg-slate-50">
            <div className="flex items-center gap-1.5 text-xs font-bold text-slate-800 uppercase tracking-wider">
              <Activity size={14} className="text-indigo-600" />
              Workflow Inspector
            </div>
          </div>

          <div className="flex-1 overflow-y-auto p-4 space-y-4">
            {/* Input Context Box */}
            <div className="space-y-1.5">
              <label className="text-xs font-semibold text-slate-700 flex items-center justify-between">
                <span>Input Context (Payload)</span>
                <span className="text-[10px] text-slate-400 font-normal">Passed to AI nodes</span>
              </label>
              <textarea
                value={inputContext}
                onChange={(e) => setInputContext(e.target.value)}
                rows={3}
                className="w-full rounded-md border border-slate-300 p-2 text-xs text-slate-800 placeholder-slate-400 focus:outline-none focus:ring-1 focus:ring-indigo-500 shadow-sm"
                placeholder="Enter raw text, email, incident or request..."
              />
            </div>

            {/* Selected Node Editor */}
            {selectedNode && (
              <Card className="border-indigo-100 bg-indigo-50/40">
                <CardHeader className="pb-2">
                  <CardTitle className="text-xs font-bold text-indigo-950 flex items-center gap-1.5">
                    <Settings size={13} className="text-indigo-600" />
                    Configure Node: {selectedNode.id}
                  </CardTitle>
                </CardHeader>
                <CardContent className="space-y-2.5">
                  <div>
                    <label className="text-[11px] font-semibold text-slate-600">Node Label</label>
                    <Input
                      value={selectedNode.data.label || ""}
                      onChange={(e) => handleUpdateSelectedNode("label", e.target.value)}
                      className="h-8 text-xs bg-white"
                    />
                  </div>

                  {selectedNode.type === "decision" && (
                    <div>
                      <label className="text-[11px] font-semibold text-slate-600">AI Triage Prompt</label>
                      <textarea
                        value={selectedNode.data.prompt || ""}
                        onChange={(e) => handleUpdateSelectedNode("prompt", e.target.value)}
                        rows={3}
                        className="w-full rounded-md border border-slate-300 p-2 text-xs bg-white text-slate-800 focus:outline-none focus:ring-1 focus:ring-indigo-500"
                        placeholder="Evaluation question..."
                      />
                    </div>
                  )}
                </CardContent>
              </Card>
            )}

            {/* Live Execution Results Trace */}
            {executionResult && (
              <div className="space-y-2 pt-2 border-t border-slate-200">
                <div className="flex items-center justify-between">
                  <span className="text-xs font-bold text-slate-800 flex items-center gap-1.5">
                    <Terminal size={14} className="text-emerald-600" />
                    Execution Trace
                  </span>
                  <Badge variant="outline" className="text-[10px] font-mono">
                    {executionResult.run_id}
                  </Badge>
                </div>

                <div className="rounded-md bg-slate-900 p-3 text-xs text-slate-100 font-mono space-y-2">
                  <div className="text-[11px] text-slate-400">
                    Status: <span className="text-emerald-400 font-bold">{executionResult.status}</span> &bull; Time: {executionResult.total_latency_ms}ms
                  </div>

                  <div className="space-y-1.5 mt-2">
                    {executionResult.trace?.map((step, idx) => (
                      <div key={idx} className="border-b border-slate-800 pb-1.5 last:border-0">
                        <div className="flex items-center justify-between text-[11px]">
                          <span className="text-indigo-400 font-bold">Step {step.step}: {step.node_label}</span>
                          {step.decision && (
                            <span className={step.decision === "YES" ? "text-emerald-400 font-bold" : "text-rose-400 font-bold"}>
                              [{step.decision}]
                            </span>
                          )}
                        </div>
                        {step.rationale && (
                          <p className="text-[10px] text-slate-400 italic mt-0.5">{step.rationale}</p>
                        )}
                        {step.latency_ms > 0 && (
                          <div className="text-[9px] text-slate-500">latency: {step.latency_ms}ms</div>
                        )}
                      </div>
                    ))}
                  </div>

                  {executionResult.outcome && (
                    <div className="pt-2 border-t border-slate-700 text-emerald-300 font-bold text-xs flex items-center gap-1">
                      <span>&rarr; Terminal Outcome:</span>
                      <span>{executionResult.outcome}</span>
                    </div>
                  )}
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
