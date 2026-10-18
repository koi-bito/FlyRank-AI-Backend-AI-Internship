import React from "react";
import { cn } from "../../lib/utils";

export const Button = React.forwardRef(({
  className,
  variant = "default",
  size = "default",
  children,
  ...props
}, ref) => {
  const base = "inline-flex items-center justify-center font-medium transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-offset-2 disabled:opacity-50 disabled:pointer-events-none rounded-md cursor-pointer";
  
  const variants = {
    default: "btn-primary",
    secondary: "btn-secondary",
    outline: "btn-outline",
    destructive: "btn-destructive",
    ghost: "btn-ghost",
  };

  const sizes = {
    default: "h-9 px-4 py-2 text-sm",
    sm: "h-8 px-3 text-xs",
    lg: "h-10 px-6 text-base",
    icon: "h-9 w-9 p-0",
  };

  return (
    <button
      ref={ref}
      className={cn(base, variants[variant], sizes[size], className)}
      {...props}
    >
      {children}
    </button>
  );
});

Button.displayName = "Button";
