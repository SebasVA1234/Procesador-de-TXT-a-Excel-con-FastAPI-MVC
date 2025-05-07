import React, { useState, useRef } from "react";
import "./App.css";

function App() {
  const [selectedCase, setSelectedCase] = useState("pagos");
  const [fileName, setFileName] = useState(null);
  const [statusMessage, setStatusMessage] = useState("");
  const [statusColor, setStatusColor] = useState("");
  const [isProcessing, setIsProcessing] = useState(false);
  const fileInputRef = useRef(null);

  const handleDrop = (e) => {
    e.preventDefault();
    const droppedFile = e.dataTransfer.files[0];
    if (droppedFile && droppedFile.name.endsWith(".txt")) {
      fileInputRef.current.files = e.dataTransfer.files;
      setFileName(droppedFile.name);
      setStatusMessage("");
    } else {
      showError("Error: Solo se permiten archivos .txt");
    }
  };

  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0];
    if (selectedFile && selectedFile.name.endsWith(".txt")) {
      setFileName(selectedFile.name);
      setStatusMessage("");
    } else {
      showError("Error: Solo se permiten archivos .txt");
    }
  };

  const showError = (message) => {
    setStatusMessage(message);
    setStatusColor("text-red-600");
    setFileName(null);
    fileInputRef.current.value = "";
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!fileInputRef.current.files.length) {
      showError("Por favor selecciona un archivo primero.");
      return;
    }

    setIsProcessing(true);
    setStatusMessage("Procesando archivo...");
    setStatusColor("text-blue-600");

    // Aquí puedes usar fetch si deseas enviar al backend
    setTimeout(() => {
      const success = true; // Simulación
      setIsProcessing(false);
      if (success) {
        setStatusMessage("✅ Archivo procesado exitosamente.");
        setStatusColor("text-green-600");
      } else {
        showError("❌ Error al procesar el archivo.");
      }
    }, 1500);
  };

  return (
    <div className="bg-gradient-to-r from-blue-50 via-white to-blue-50 min-h-screen flex items-center justify-center p-6">
      <div className="bg-white shadow-lg rounded-xl max-w-md w-full p-8 font-[Inter,sans-serif]">
        <h1 className="text-3xl font-semibold text-slate-900 mb-6">Procesador de Archivos TXT</h1>

        <form onSubmit={handleSubmit} className="space-y-6">
          {/* Tipo de archivo */}
          <div>
            <label className="block mb-2 font-medium text-slate-700">Seleccione tipo de archivo</label>
            <select
              value={selectedCase}
              onChange={(e) => setSelectedCase(e.target.value)}
              className="w-full border border-blue-300 rounded-lg px-4 py-2 text-slate-700 focus:outline-none focus:ring-2 focus:ring-blue-400 transition"
              required
            >
              <option value="pagos">Info de pagos a proveedores</option>
              <option value="compras">Info de compra orden</option>
            </select>
          </div>

          {/* Área de carga */}
          <div>
            <label className="block mb-2 font-medium text-slate-700">Archivo cargado</label>
            <div
              role="button"
              tabIndex={0}
              onClick={() => fileInputRef.current.click()}
              onKeyDown={(e) => (e.key === "Enter" || e.key === " " ? fileInputRef.current.click() : null)}
              onDrop={handleDrop}
              onDragOver={(e) => e.preventDefault()}
              onDragLeave={(e) => e.preventDefault()}
              className="w-full border-2 border-dashed border-blue-300 rounded-lg p-4 text-center cursor-pointer text-slate-500 hover:border-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-400 transition"
            >
              {fileName || "Haz clic aquí o arrastra el archivo para cargarlo"}
            </div>
            <input
              type="file"
              accept=".txt"
              className="hidden"
              ref={fileInputRef}
              onChange={handleFileChange}
              required
            />
          </div>

          {/* Botón de envío */}
          <div>
            <button
              type="submit"
              disabled={!fileName || isProcessing}
              className="w-full bg-blue-600 text-white font-semibold rounded-lg px-4 py-3 hover:bg-blue-700 transition disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {isProcessing ? "Procesando..." : "Convertir"}
            </button>
          </div>

          {/* Mensaje de estado */}
          <div className={`text-center text-sm font-medium mt-2 min-h-[1.5rem] ${statusColor}`}>
            {statusMessage}
          </div>
        </form>
      </div>
    </div>
  );
}

export default App;
