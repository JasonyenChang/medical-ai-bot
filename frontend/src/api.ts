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