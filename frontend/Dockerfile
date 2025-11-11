# ===============================
# Frontend Dockerfile (Vue + Vite)
# ===============================
FROM node:22-alpine AS build

WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

# --- Nginx Stage ---
FROM nginx:1.27-alpine

# 移除預設頁面並複製前端打包成果
RUN rm -rf /usr/share/nginx/html/*
COPY --from=build /app/dist /usr/share/nginx/html

# 複製 nginx.conf
COPY nginx.conf /etc/nginx/conf.d/default.conf

# 自訂 nginx.conf 可選
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
