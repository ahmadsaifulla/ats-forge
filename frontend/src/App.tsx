import { Navigate, Route, Routes } from "react-router-dom";
import { AppShell } from "./components/AppShell";
import { AnalysisPage } from "./pages/AnalysisPage";
import { OptimizedResumePage } from "./pages/OptimizedResumePage";
import { UploadPage } from "./pages/UploadPage";

function App() {
  return (
    <AppShell>
      <Routes>
        <Route path="/" element={<UploadPage />} />
        <Route path="/analysis" element={<AnalysisPage />} />
        <Route path="/optimized" element={<OptimizedResumePage />} />
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </AppShell>
  );
}

export default App;
