"use client";

import type { AnchorHTMLAttributes, ReactNode } from "react";
import { trackEvent, trackHref, type AnalyticsEvent } from "@/lib/analytics";

type OutboundLinkProps = AnchorHTMLAttributes<HTMLAnchorElement> & {
  children: ReactNode;
  location: string;
  eventName?: AnalyticsEvent;
};

export default function OutboundLink({
  children,
  location,
  eventName,
  onClick,
  href,
  ...rest
}: OutboundLinkProps) {
  return (
    <a
      href={href}
      {...rest}
      onClick={(event) => {
        if (eventName) {
          trackEvent(eventName, { link_location: location });
        } else if (typeof href === "string") {
          trackHref(href, location);
        }
        onClick?.(event);
      }}
    >
      {children}
    </a>
  );
}
