import React from "react";
import { getBezierPath, EdgeLabelRenderer, BaseEdge } from "reactflow";

export function YesNoEdge({
  id,
  sourceX,
  sourceY,
  targetX,
  targetY,
  sourcePosition,
  targetPosition,
  data,
  markerEnd,
  selected
}) {
  const [edgePath, labelX, labelY] = getBezierPath({
    sourceX,
    sourceY,
    sourcePosition,
    targetX,
    targetY,
    targetPosition,
  });

  const branch = (data?.branch || "DEFAULT").toUpperCase();
  const isActive = data?.isActive;

  const getEdgeStyle = () => {
    if (branch === "YES") {
      return {
        stroke: isActive ? "#059669" : "#10B981",
        strokeWidth: isActive ? 3 : 2,
      };
    }
    if (branch === "NO") {
      return {
        stroke: isActive ? "#E11D48" : "#F43F5E",
        strokeWidth: isActive ? 3 : 2,
      };
    }
    return {
      stroke: isActive ? "#6366F1" : "#94A3B8",
      strokeWidth: isActive ? 3 : 2,
    };
  };

  const getBadgeClass = () => {
    if (branch === "YES") return "edge-badge edge-yes";
    if (branch === "NO") return "edge-badge edge-no";
    return "edge-badge edge-default";
  };

  return (
    <>
      <BaseEdge
        id={id}
        path={edgePath}
        markerEnd={markerEnd}
        style={getEdgeStyle()}
      />
      <EdgeLabelRenderer>
        <div
          style={{
            position: "absolute",
            transform: `translate(-50%, -50%) translate(${labelX}px,${labelY}px)`,
            pointerEvents: "all",
          }}
          className={getBadgeClass()}
        >
          {branch}
        </div>
      </EdgeLabelRenderer>
    </>
  );
}
