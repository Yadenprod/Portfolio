FROM node:18-alpine

WORKDIR /app

COPY package*.json ./

RUN npm install

COPY . .

RUN npm run build

EXPOSE 3000

ENV NODE_ENV=production
ENV MONGODB_URI=mongodb://mongodb:27017/cspanel
ENV NEXTAUTH_URL=http://localhost:3000
ENV NEXTAUTH_SECRET=your_secret_key_here

CMD ["npm", "start"] 