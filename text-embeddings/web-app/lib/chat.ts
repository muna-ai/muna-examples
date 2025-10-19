export interface Message {
  sender: "user" | "assistant";
  content?: string;
  loading?: boolean;
}