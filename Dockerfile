# Use the official Node.js image as the base image
FROM node:20.16.0 as base

# Set the working directory
WORKDIR /app

# Copy package.json and package-lock.json
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy environment configuration
COPY .env.local ./

# Copy Next.js configuration
COPY next.config.mjs ./

# Expose the application port
EXPOSE 3000

# Use the base image to create a builder stage
FROM base as builder

# Set the working directory
WORKDIR /app

# Copy the entire project
COPY . .

# Ensure node_modules/.bin is in the PATH
ENV PATH /app/node_modules/.bin:$PATH

# Fix permissions on node_modules/.bin/next
RUN chmod +x /app/node_modules/.bin/next


# Install additional dependencies
RUN apt-get update && apt-get install -y curl git

# Build the Next.js application
RUN npm run build

# Use the base image to create a production stage
FROM base as production

# Set the working directory
WORKDIR /app

# Set the environment to production
ENV NODE_ENV=production

# Create the nextjs user and group
RUN groupadd -r nextjs && useradd -r -g nextjs nextjs

# Install production dependencies
RUN npm ci

# Copy the built application from the builder stage
COPY --from=builder --chown=nextjs:nextjs /app/.next ./.next

# Change ownership of the application files
RUN chown -R nextjs:nextjs /app

# Switch to the nextjs user
USER nextjs

# Start the application
CMD ["npm", "start"]