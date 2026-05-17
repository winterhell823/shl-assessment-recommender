"use client";

import { useEffect, useRef, useCallback, useState } from "react";
import { cn } from "@/lib/utils";
import {
    SendIcon,
    LoaderIcon,
    Sparkles,
    ExternalLink,
    RefreshCw,
    AlertCircle,
    User,
    Bot,
} from "lucide-react";
import { motion, AnimatePresence } from "framer-motion";
import * as React from "react";
import { sendMessageToAPI, type Message } from "@/lib/api";

interface UseAutoResizeTextareaProps {
    minHeight: number;
    maxHeight?: number;
}

function useAutoResizeTextarea({
    minHeight,
    maxHeight,
}: UseAutoResizeTextareaProps) {
    const textareaRef = useRef<HTMLTextAreaElement>(null);

    const adjustHeight = useCallback(
        (reset?: boolean) => {
            const textarea = textareaRef.current;
            if (!textarea) return;

            if (reset) {
                textarea.style.height = `${minHeight}px`;
                return;
            }

            textarea.style.height = `${minHeight}px`;
            const newHeight = Math.max(
                minHeight,
                Math.min(
                    textarea.scrollHeight,
                    maxHeight ?? Number.POSITIVE_INFINITY
                )
            );

            textarea.style.height = `${newHeight}px`;
        },
        [minHeight, maxHeight]
    );

    useEffect(() => {
        const textarea = textareaRef.current;
        if (textarea) {
            textarea.style.height = `${minHeight}px`;
        }
    }, [minHeight]);

    useEffect(() => {
        const handleResize = () => adjustHeight();
        window.addEventListener("resize", handleResize);
        return () => window.removeEventListener("resize", handleResize);
    }, [adjustHeight]);

    return { textareaRef, adjustHeight };
}

interface CommandSuggestion {
    icon: React.ReactNode;
    label: string;
    description: string;
    prefix: string;
}

interface TextareaProps
  extends React.TextareaHTMLAttributes<HTMLTextAreaElement> {
  containerClassName?: string;
  showRing?: boolean;
}

const Textarea = React.forwardRef<HTMLTextAreaElement, TextareaProps>(
  ({ className, containerClassName, showRing = true, ...props }, ref) => {

    
    return (
      <div className={cn("relative w-full", containerClassName)}>
        <textarea
          className={cn(
            "flex min-h-[50px] w-full rounded-xl border border-green-200/50 bg-white/75 px-4 py-3 text-sm shadow-sm backdrop-blur-md",
            "transition-all duration-200 ease-in-out",
            "placeholder:text-gray-400 text-gray-800",
            "disabled:cursor-not-allowed disabled:opacity-50",
            "focus-visible:outline-none focus:border-green-400 focus:ring-1 focus:ring-green-400/50",
            className
          )}
          ref={ref}

          {...props}
        />
      </div>
    );
  }
);
Textarea.displayName = "Textarea";

interface ChatMessage {
    id: string;
    role: "user" | "assistant";
    content: string;
    recommendations?: Array<{
        name: string;
        url: string;
        test_type?: string;
    }>;
}

export function AnimatedAIChat() {
    const [value, setValue] = useState("");
    const [chatHistory, setChatHistory] = useState<ChatMessage[]>([]);
    const [isTyping, setIsTyping] = useState(false);
    const [error, setError] = useState<string | null>(null);
    
    const messagesEndRef = useRef<HTMLDivElement>(null);
    const { textareaRef, adjustHeight } = useAutoResizeTextarea({
        minHeight: 50,
        maxHeight: 150,
    });

    const commandSuggestions: CommandSuggestion[] = [
        { 
            icon: <Sparkles className="w-4 h-4" />, 
            label: "Recommend Sales Test", 
            description: "Assessments for B2B sales professionals", 
            prefix: "Suggest SHL tests for a Senior B2B Sales Executive with 5+ years of experience." 
        },
        { 
            icon: <Sparkles className="w-4 h-4" />, 
            label: "Developer Assessments", 
            description: "Assessments for Software Engineers", 
            prefix: "What assessments should I use for hiring a Mid-Level Frontend React Developer?" 
        },
        { 
            icon: <Sparkles className="w-4 h-4" />, 
            label: "Graduate Cognitive Tests", 
            description: "General cognitive ability assessments", 
            prefix: "Recommend cognitive and aptitude tests suitable for a Graduate Trainee program." 
        },
        { 
            icon: <Sparkles className="w-4 h-4" />, 
            label: "Managerial Leadership", 
            description: "Leadership capability assessments", 
            prefix: "I am hiring a Operations Manager. What leadership or personality tests do you recommend?" 
        },
    ];

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
    };

    useEffect(() => {
        scrollToBottom();
    }, [chatHistory, isTyping]);

    const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
        if (e.key === "Enter" && !e.shiftKey) {
            e.preventDefault();
            if (value.trim() && !isTyping) {
                handleSendMessage(value.trim());
            }
        }
    };

    const handleSendMessage = async (text: string) => {
        if (!text) return;
        setError(null);

        const userMsg: ChatMessage = {
            id: `msg-${Date.now()}-user`,
            role: "user",
            content: text,
        };

        setChatHistory(prev => [...prev, userMsg]);
        setValue("");
        adjustHeight(true);
        setIsTyping(true);

        try {
            // Prepare API format
            const apiMessages: Message[] = [...chatHistory, userMsg].map(msg => ({
                role: msg.role === "user" ? "user" : "assistant",
                content: msg.content
            }));

            // Call API
            const response = await sendMessageToAPI(apiMessages);

            const assistantMsg: ChatMessage = {
                id: `msg-${Date.now()}-assistant`,
                role: "assistant",
                content: response.reply,
                recommendations: response.recommendations,
            };

            setChatHistory(prev => [...prev, assistantMsg]);
        } catch (err: any) {
            console.error("API Error details:", err);
            setError(err.message || "Something went wrong. Please make sure the backend is running.");
        } finally {
            setIsTyping(false);
        }
    };

    const selectCommandSuggestion = (suggestion: CommandSuggestion) => {
        setValue(suggestion.prefix);
        textareaRef.current?.focus();
    };

    const resetChat = () => {
        setChatHistory([]);
        setError(null);
        setValue("");
    };

    return (
        <div className="min-h-screen flex flex-col w-full bg-gradient-to-br from-white via-green-50/30 to-emerald-50/20 text-gray-900 relative overflow-hidden">
            {/* Visual background accents */}
            <div className="absolute inset-0 w-full h-full overflow-hidden pointer-events-none z-0">
                <div className="absolute top-0 left-1/4 w-[30rem] h-[30rem] bg-green-500/5 rounded-full filter blur-[128px]" />
                <div className="absolute bottom-0 right-1/4 w-[30rem] h-[30rem] bg-emerald-500/5 rounded-full filter blur-[128px]" />
            </div>

            {/* Header */}
            <header className="relative z-10 w-full backdrop-blur-md bg-white/70 border-b border-green-100 px-6 py-4 flex items-center justify-between">
                <div className="flex items-center gap-3">
                    {/* eslint-disable-next-line @next/next/no-img-element */}
                    <img 
                        src="/shl-logo.svg" 
                        alt="SHL Logo" 
                        className="h-8 w-auto object-contain"
                    />
                    <div>
                        <h1 className="font-semibold text-gray-800 text-sm tracking-tight">SHL Assessment Recommender</h1>
                        <p className="text-[10px] text-green-600 font-medium flex items-center gap-1">
                            <span className="w-1.5 h-1.5 rounded-full bg-green-500 animate-pulse" />
                            Agent Active
                        </p>
                    </div>
                </div>

                {chatHistory.length > 0 && (
                    <button
                        onClick={resetChat}
                        className="text-xs text-gray-500 hover:text-green-600 flex items-center gap-1.5 px-3 py-1.5 rounded-lg hover:bg-green-50 transition-all font-medium border border-gray-100"
                    >
                        <RefreshCw className="w-3.5 h-3.5" />
                        Clear Chat
                    </button>
                )}
            </header>

            {/* Main Chat Area */}
            <div className="flex-1 overflow-y-auto relative z-10 py-6 px-4 md:px-6 flex flex-col items-center">
                <div className="w-full max-w-3xl flex-1 flex flex-col">
                    {chatHistory.length === 0 ? (
                        /* Welcome Screen */
                        <div className="flex-1 flex flex-col justify-center items-center py-12 space-y-12">
                            <motion.div
                                initial={{ opacity: 0, y: 15 }}
                                animate={{ opacity: 1, y: 0 }}
                                transition={{ duration: 0.6 }}
                                className="text-center space-y-4"
                            >
                                <div className="inline-flex p-3 rounded-2xl bg-green-50 text-green-600 shadow-inner mb-2">
                                    <Sparkles className="w-8 h-8 animate-pulse" />
                                </div>
                                <h2 className="text-3xl md:text-4xl font-semibold tracking-tight text-gray-800">
                                    Find the perfect <span className="bg-clip-text text-transparent bg-gradient-to-r from-green-700 to-emerald-600">SHL Assessment</span>
                                </h2>
                                <p className="text-sm text-gray-500 max-w-md mx-auto">
                                    I will analyze your role requirements, target seniority level, and required skills to recommend exact SHL catalog assessments.
                                </p>
                            </motion.div>

                            {/* Suggestions Grid */}
                            <motion.div 
                                className="grid grid-cols-1 md:grid-cols-2 gap-4 w-full max-w-2xl"
                                initial={{ opacity: 0 }}
                                animate={{ opacity: 1 }}
                                transition={{ delay: 0.2 }}
                            >
                                {commandSuggestions.map((suggestion, index) => (
                                    <button
                                        key={index}
                                        onClick={() => selectCommandSuggestion(suggestion)}
                                        className="text-left p-4 bg-white/70 hover:bg-white hover:border-green-300 rounded-2xl border border-green-100/80 shadow-sm hover:shadow-md transition-all group flex gap-3 relative"
                                    >
                                        <div className="p-2 rounded-xl bg-green-50 text-green-600 group-hover:bg-green-100 transition-colors h-fit mt-0.5">
                                            {suggestion.icon}
                                        </div>
                                        <div>
                                            <h4 className="font-semibold text-gray-800 text-sm group-hover:text-green-700 transition-colors">
                                                {suggestion.label}
                                            </h4>
                                            <p className="text-xs text-gray-500 mt-0.5">
                                                {suggestion.description}
                                            </p>
                                        </div>
                                    </button>
                                ))}
                            </motion.div>
                        </div>
                    ) : (
                        /* Message List */
                        <div className="space-y-6 py-4 flex-1">
                            {chatHistory.map((message) => (
                                <motion.div
                                    key={message.id}
                                    className={cn(
                                        "flex gap-4 w-full",
                                        message.role === "user" ? "justify-end" : "justify-start"
                                    )}
                                    initial={{ opacity: 0, y: 10 }}
                                    animate={{ opacity: 1, y: 0 }}
                                >
                                    {/* Bot Avatar */}
                                    {message.role === "assistant" && (
                                        <div className="w-8 h-8 rounded-lg bg-green-100 text-green-700 flex items-center justify-center shadow-sm shrink-0">
                                            <Bot className="w-4 h-4" />
                                        </div>
                                    )}

                                    <div className={cn(
                                        "max-w-[85%] rounded-2xl p-4 shadow-sm",
                                        message.role === "user" 
                                            ? "bg-green-600 text-white font-medium rounded-tr-none shadow-green-100" 
                                            : "bg-white/90 border border-green-100 rounded-tl-none text-gray-800"
                                    )}>
                                        <p className="text-sm leading-relaxed whitespace-pre-wrap">{message.content}</p>

                                        {/* Recommendations Grid inside Assistant bubble */}
                                        {message.role === "assistant" && message.recommendations && message.recommendations.length > 0 && (
                                            <div className="mt-4 pt-4 border-t border-green-50 space-y-3">
                                                <h5 className="text-xs font-semibold text-green-700 tracking-wider uppercase flex items-center gap-1.5">
                                                    <Sparkles className="w-3 h-3" />
                                                    Recommended Assessments
                                                </h5>
                                                <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                                                    {message.recommendations.map((rec, i) => (
                                                        <a
                                                            key={i}
                                                            href={rec.url}
                                                            target="_blank"
                                                            rel="noopener noreferrer"
                                                            className="flex flex-col justify-between p-3 rounded-xl border border-green-100 bg-green-50/20 hover:bg-green-50/50 hover:border-green-200 transition-all group shadow-inner"
                                                        >
                                                            <div>
                                                                <span className="text-[10px] font-bold text-green-600 bg-green-100/50 px-2 py-0.5 rounded-full uppercase">
                                                                    {rec.test_type || "SHL Assessment"}
                                                                </span>
                                                                <h6 className="font-semibold text-xs text-gray-800 mt-2 group-hover:text-green-700 transition-colors line-clamp-2">
                                                                    {rec.name}
                                                                </h6>
                                                            </div>
                                                            <div className="flex items-center gap-1 text-[10px] text-green-600 font-semibold mt-3 pt-2 border-t border-green-100/50">
                                                                View Details
                                                                <ExternalLink className="w-2.5 h-2.5 group-hover:translate-x-0.5 transition-transform" />
                                                            </div>
                                                        </a>
                                                    ))}
                                                </div>
                                            </div>
                                        )}
                                    </div>

                                    {/* User Avatar */}
                                    {message.role === "user" && (
                                        <div className="w-8 h-8 rounded-lg bg-green-600 text-white flex items-center justify-center shadow-sm shrink-0">
                                            <User className="w-4 h-4" />
                                        </div>
                                    )}
                                </motion.div>
                            ))}

                            {/* Typing Indicator */}
                            {isTyping && (
                                <motion.div
                                    className="flex gap-4 w-full justify-start"
                                    initial={{ opacity: 0 }}
                                    animate={{ opacity: 1 }}
                                >
                                    <div className="w-8 h-8 rounded-lg bg-green-100 text-green-700 flex items-center justify-center shadow-sm shrink-0">
                                        <Bot className="w-4 h-4 animate-pulse" />
                                    </div>
                                    <div className="bg-white/90 border border-green-100 rounded-2xl rounded-tl-none p-4 shadow-sm flex items-center gap-2">
                                        <LoaderIcon className="w-4 h-4 text-green-600 animate-spin" />
                                        <span className="text-xs text-gray-500 font-medium">SHL recommender agent is thinking...</span>
                                    </div>
                                </motion.div>
                            )}

                            <div ref={messagesEndRef} />
                        </div>
                    )}
                </div>
            </div>

            {/* Error Message */}
            <AnimatePresence>
                {error && (
                    <motion.div 
                        className="relative z-20 max-w-xl mx-auto mb-4 mx-4 p-4 rounded-xl bg-red-50 border border-red-200 text-red-700 shadow-sm flex gap-3 items-start"
                        initial={{ opacity: 0, y: 10 }}
                        animate={{ opacity: 1, y: 0 }}
                        exit={{ opacity: 0 }}
                    >
                        <AlertCircle className="w-5 h-5 shrink-0 mt-0.5" />
                        <div>
                            <h4 className="font-semibold text-sm">Connection Error</h4>
                            <p className="text-xs text-red-600/90 mt-1">{error}</p>
                            <button
                                onClick={() => handleSendMessage(chatHistory[chatHistory.length - 1]?.content)}
                                className="text-xs font-bold text-red-800 underline hover:text-red-950 mt-2 block"
                            >
                                Retry Last Message
                            </button>
                        </div>
                    </motion.div>
                )}
            </AnimatePresence>

            {/* Input Form */}
            <footer className="relative z-10 w-full backdrop-blur-md bg-white/70 border-t border-green-100 p-4 flex justify-center">
                <div className="w-full max-w-3xl flex items-center gap-3 relative">
                    <Textarea
                        ref={textareaRef}
                        value={value}
                        onChange={(e) => {
                            setValue(e.target.value);
                            adjustHeight();
                        }}
                        onKeyDown={handleKeyDown}
                        placeholder={isTyping ? "AI agent is thinking..." : "Type assessment details (e.g. 'hiring React developers Mid-level')..."}
                        className="pr-12"
                        disabled={isTyping}
                    />
                    <button
                        onClick={() => handleSendMessage(value.trim())}
                        disabled={!value.trim() || isTyping}
                        className={cn(
                            "absolute right-2.5 top-1/2 -translate-y-1/2 p-2 rounded-xl transition-all shadow-md",
                            value.trim() && !isTyping
                                ? "bg-green-600 hover:bg-green-700 text-white shadow-green-200"
                                : "bg-gray-100 text-gray-400 cursor-not-allowed shadow-none"
                        )}
                    >
                        <SendIcon className="w-4 h-4" />
                    </button>
                </div>
            </footer>
        </div>
    );
}
