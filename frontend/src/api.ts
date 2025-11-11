import axios from "axios";

const api = axios.create({
    baseURL:
        import.meta.env.MODE === "development"
            ? "http://localhost:8000"
            : "/",
});

export async function getTrendingProducts() {
    const { data } = await api.get("/api/trending-products");
    return data;
}

export async function askDoctorQuestion(question: string) {
    const { data } = await api.post(
        "/api/chat/",
        {
            question
        }
    );
    return data.answer;
}

export async function askDoctorQuestionStream(
    question: string,
    onChunk?: (text: string) => void
): Promise<string> {
    const response = await fetch(`${api.defaults.baseURL}/api/chat/stream/`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question }),
    });

    if (!response.ok || !response.body) {
        throw new Error("Network or server error.");
    }

    const reader = response.body.getReader();
    const decoder = new TextDecoder("utf-8");
    let result = "";

    while (true) {
        const { done, value } = await reader.read();
        if (done) break;

        const chunk = decoder.decode(value);
        if (chunk.includes("[END]")) break;

        result += chunk;
        if (onChunk) onChunk(chunk); // ✅ 即時回傳
    }

    return result;
}