import React from 'react';
import ReactDOM from 'react-dom';

interface ModalProps {
  isOpen: boolean;
  onClose: () => void;
  title: string;
  children: React.ReactNode;
  footer?: React.ReactNode;
}

const Modal: React.FC<ModalProps> = ({ isOpen, onClose, title, children, footer }) => {
  if (!isOpen) return null;

  return ReactDOM.createPortal(
    <div className="fixed inset-0 bg-gray-900 bg-opacity-75 flex items-center justify-center z-50">
      <div className="bg-gray-800 rounded-lg shadow-xl w-11/12 md:max-w-md mx-auto p-6 relative">
        {/* Header */}
        <div className="flex justify-between items-center pb-3 border-b border-gray-700 mb-4">
          <h3 className="text-2xl font-bold text-white">{title}</h3>
          <button onClick={onClose} className="text-gray-400 hover:text-gray-200 text-3xl leading-none font-semibold focus:outline-none">
            &times;
          </button>
        </div>

        {/* Body */}
        <div className="text-gray-300 mb-4">
          {children}
        </div>

        {/* Footer */}
        {footer && (
          <div className="flex justify-end pt-3 border-t border-gray-700 mt-4">
            {footer}
          </div>
        )}
      </div>
    </div>,
    document.body
  );
};

export default Modal;
