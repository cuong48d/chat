import { atomWithStorage } from "jotai/utils"

export const EnterKeyBehaviourAtom = atomWithStorage<"new-line" | "send-message">("chat-enter-key-behaviour", "send-message", undefined, { getOnInit: true })

export const QuickEmojisAtom = atomWithStorage<string[]>("chat-quick-emojis", ["👍", "✅", "👀", "🎉"])