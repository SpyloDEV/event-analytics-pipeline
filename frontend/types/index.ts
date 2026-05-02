export type IngestionStatus = "accepted" | "rejected" | "processed" | "failed";

export type RawEvent = {
  id: string;
  eventName: string;
  userId?: string;
  status: IngestionStatus;
  country?: string;
};

export type EventSchema = {
  id: string;
  eventName: string;
  requiredProperties: string[];
  isActive: boolean;
};
