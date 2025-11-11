import axios from "axios";

const api = axios.create({
    baseURL:
        import.meta.env.MODE === "development"
            ? "http://localhost:3000"
            : "/",
});

export async function getTrendingProducts() {
    const { data } = await api.get("/api/trending-products");
    return data;
}