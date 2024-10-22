# Stage 1: Build Vite app
FROM node:18-alpine as build

WORKDIR /app

# Install dependencies
COPY package*.json ./
RUN npm install

# Copy app code and build the production app
COPY . .
RUN npm run build

# Optional: Verify the dist directory exists
RUN ls -la /app/dist

# Stage 2: Serve the Vite build using Nginx
FROM nginx:alpine

# Copy the build artifacts to the Nginx HTML directory
COPY --from=build /app/dist /usr/share/nginx/html

# Expose port 80 for Nginx
EXPOSE 80

# Start Nginx
CMD ["nginx", "-g", "daemon off;"]
