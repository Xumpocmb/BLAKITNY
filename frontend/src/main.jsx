import { createRoot } from "react-dom/client";
import "./index.css";
import App from "./App.jsx";
import { CartProvider } from "./cart/CartContext.tsx";

createRoot(document.getElementById("root")).render(
  <CartProvider>
    <App />
  </CartProvider>,
);
