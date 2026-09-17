// Top-level routes, wrapped in a RequireAuth guard that redirects to /login
// when useAuth().user is null. Routes: / (Dashboard), /accounts, /transactions,
// /budgets, /manual, /csv-import, /settings, plus the public /login.
