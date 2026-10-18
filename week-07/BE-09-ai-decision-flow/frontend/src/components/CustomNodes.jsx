import React, { memo } from "react";
import { Handle, Position } from "reactflow";
import { Sparkles, Play, CheckCircle2, AlertTriangle } from "lucide-react";

export const StartNode = memo(({ data, selected }) => {
  return (
    <div className={`node-container start-node ${selected ? "selected" : ""} ${data.isActive ? "active-pulse" : ""}`}>
      <div className="node-header">
        <Play size={14} className="node-icon text-indigo-400" />
        <span className="node-title">{data.label || "Start Trigger"}</span>
      </div>
      <div className="node-body text-xs text-slate-400">
        Intake boundary
      </div>
      <Handle
        type="source"
        position={Position.Bottom}
        id="DEFAULT"
        className="custom-handle handle-default"
      />
    </div>
  );
});

export const DecisionNode = memo(({ data, selected }) => {
  return (
    <div className={`node-container decision-node ${selected ? "selected" : ""} ${data.isActive ? "active-pulse ring-2 ring-indigo-500" : ""}`}>
      <Handle
        type="target"
        position={Position.Top}
        className="custom-handle handle-target"
      />
      <div className="node-header flex items-center justify-between">
        <div className="flex items-center gap-1.5">
          <Sparkles size={14} className="node-icon text-indigo-500" />
          <span className="node-title font-semibold text-slate-900">{data.label || "Decision Step"}</span>
        </div>
        {data.decisionResult && (
          <span className={`px-2 py-0.5 rounded text-[10px] font-bold ${data.decisionResult === 'YES' ? 'bg-emerald-100 text-emerald-800 border border-emerald-300' : 'bg-rose-100 text-rose-800 border border-rose-300'}`}>
            {data.decisionResult}
          </span>
        )}
      </div>

      <div className="node-prompt-box">
        <p className="text-xs text-slate-600 line-clamp-3 italic">
          "{data.prompt || "Is condition met?"}"
        </p>
      </div>

      <div className="node-footer flex justify-between items-center text-[11px] font-medium pt-2 border-t border-slate-100">
        <div className="flex items-center gap-1 text-emerald-600">
          <span className="w-2 h-2 rounded-full bg-emerald-500 inline-block"></span>
          <span>YES</span>
        </div>
        <div className="flex items-center gap-1 text-rose-600">
          <span>NO</span>
          <span className="w-2 h-2 rounded-full bg-rose-500 inline-block"></span>
        </div>
      </div>

      {/* YES Handle on left */}
      <Handle
        type="source"
        position={Position.Bottom}
        id="YES"
        style={{ left: "25%" }}
        className="custom-handle handle-yes"
      />
      {/* NO Handle on right */}
      <Handle
        type="source"
        position={Position.Bottom}
        id="NO"
        style={{ left: "75%" }}
        className="custom-handle handle-no"
      />
    </div>
  );
});

export const OutcomeNode = memo(({ data, selected }) => {
  const isPositive = (data.label || "").toLowerCase().includes("approve") || (data.label || "").toLowerCase().includes("resolve");
  const isEscalation = (data.label || "").toLowerCase().includes("human") || (data.label || "").toLowerCase().includes("escalat");

  return (
    <div className={`node-container outcome-node ${selected ? "selected" : ""} ${data.isActive ? "active-pulse" : ""} ${isPositive ? "outcome-positive" : isEscalation ? "outcome-warning" : "outcome-negative"}`}>
      <Handle
        type="target"
        position={Position.Top}
        className="custom-handle handle-target"
      />
      <div className="node-header flex items-center gap-1.5">
        {isPositive ? (
          <CheckCircle2 size={15} className="text-emerald-500" />
        ) : (
          <AlertTriangle size={15} className="text-amber-500" />
        )}
        <span className="node-title font-semibold">{data.label || "Outcome"}</span>
      </div>
      <div className="node-body text-xs text-slate-500 mt-1">
        Workflow Terminal Action
      </div>
    </div>
  );
});
