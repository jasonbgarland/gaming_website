# Frontend (Next.js)

This is the main web frontend for the Gaming Library Microservices monorepo, bootstrapped with [Next.js](https://nextjs.org) and [`create-next-app`](https://nextjs.org/docs/app/api-reference/cli/create-next-app). Tailwind CSS is pre-installed and ready to use.

> **Note:** This project lives in a monorepo. See the root `README.md` for overall architecture and development workflow.

## Getting Started

1. Install dependencies (if you haven't already):

   ```bash
   npm install
   # or
   yarn install
   ```

2. Start the development server:

   - From the `apps/frontend` directory:
     ```bash
     npm run dev
     # or
     yarn dev
     ```
   - Or use the VS Code task: **Run Frontend Dev Server**

3. Open [http://localhost:3000](http://localhost:3000) in your browser.

4. Edit `src/app/page.tsx` to see live updates.

## Tailwind CSS

Tailwind CSS is pre-installed and configured. Use Tailwind utility classes in your components:

```tsx
<span className="text-3xl font-bold text-blue-500">Tailwind is working!</span>
```

Configuration files:

- `tailwind.config.js`
- `postcss.config.js`
- `src/app/globals.css` (Tailwind directives)

## Monorepo & Project Structure

- This frontend lives in `apps/frontend`.
- See the root `README.md` for backend, database, and shared code details.

## Learn More

## Resources

- [Next.js Documentation](https://nextjs.org/docs)
- [Tailwind CSS Documentation](https://tailwindcss.com/docs)
- [Monorepo root README](../../README.md)

## Environment Variables for API Endpoints

This frontend uses environment variables to configure backend API endpoints for each microservice. These variables must be set in a `.env` file in the `apps/frontend` directory (or at the project root if using a monorepo-wide `.env`).

**Required variables:**

```
NEXT_PUBLIC_AUTH_API_URL=http://localhost:8001
NEXT_PUBLIC_GAME_API_URL=http://localhost:8002
```

- The `NEXT_PUBLIC_` prefix is required for variables to be available in the browser.
- Update these URLs as needed for your local, staging, or production environments.
- If you add an API gateway, you can update these variables to point to the gateway instead.

**Example `.env` file:**

```
NEXT_PUBLIC_AUTH_API_URL=http://localhost:8001
NEXT_PUBLIC_GAME_API_URL=http://localhost:8002
```

If these variables are not set, authentication and game-related features will not work.
