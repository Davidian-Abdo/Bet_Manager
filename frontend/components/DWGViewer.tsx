import React, { useEffect, useRef } from "react";

interface DWGViewerProps {
  fileUrl: string;
}

const DWGViewer: React.FC<DWGViewerProps> = ({ fileUrl }) => {
  const viewerRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (!fileUrl) return;

    // Example: using Autodesk Viewer or third-party DWG renderer
    const initViewer = async () => {
      try {
        console.log("Loading DWG file:", fileUrl);
        // Here you can integrate your DWG renderer library
      } catch (error) {
        console.error("Failed to load DWG:", error);
      }
    };

    initViewer();
  }, [fileUrl]);

  return (
    <div
      ref={viewerRef}
      className="w-full h-full bg-gray-100 rounded-2xl shadow-sm"
    >
      <p className="text-center text-gray-500 mt-8">DWG Viewer Placeholder</p>
    </div>
  );
};

export default DWGViewer;