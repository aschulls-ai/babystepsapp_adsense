import React, { useState, createContext, useContext } from 'react';
import { ChevronDown } from 'lucide-react';

const SelectContext = createContext();

const Select = ({ children, value, onValueChange, defaultValue, disabled = false }) => {
  const [isOpen, setIsOpen] = useState(false);
  const [selectedValue, setSelectedValue] = useState(value || defaultValue || '');

  const handleSelect = (newValue) => {
    setSelectedValue(newValue);
    setIsOpen(false);
    if (onValueChange) {
      onValueChange(newValue);
    }
  };

  return (
    <SelectContext.Provider value={{
      isOpen,
      setIsOpen,
      selectedValue: value || selectedValue,
      handleSelect,
      disabled
    }}>
      <div className="relative">
        {children}
      </div>
    </SelectContext.Provider>
  );
};

const SelectTrigger = ({ children, className = '', ...props }) => {
  const { isOpen, setIsOpen, disabled } = useContext(SelectContext);

  return (
    <button
      type="button"
      onClick={() => !disabled && setIsOpen(!isOpen)}
      disabled={disabled}
      className={`
        flex items-center justify-between w-full px-3 py-2 text-left bg-white border border-gray-300 rounded-md shadow-sm
        focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500
        ${disabled ? 'bg-gray-50 text-gray-500 cursor-not-allowed' : 'hover:border-gray-400 cursor-pointer'}
        ${className}
      `}
      {...props}
    >
      {children}
      <ChevronDown className={`w-4 h-4 transition-transform ${isOpen ? 'rotate-180' : ''}`} />
    </button>
  );
};

const SelectContent = ({ children, className = '' }) => {
  const { isOpen } = useContext(SelectContext);

  if (!isOpen) return null;

  return (
    <div className={`
      absolute z-50 w-full mt-1 bg-white border border-gray-300 rounded-md shadow-lg max-h-60 overflow-auto
      ${className}
    `}>
      {children}
    </div>
  );
};

const SelectItem = ({ children, value, className = '' }) => {
  const { handleSelect, selectedValue } = useContext(SelectContext);
  const isSelected = selectedValue === value;

  return (
    <div
      onClick={() => handleSelect(value)}
      className={`
        px-3 py-2 cursor-pointer hover:bg-blue-50 hover:text-blue-900
        ${isSelected ? 'bg-blue-100 text-blue-900' : 'text-gray-900'}
        ${className}
      `}
    >
      {children}
    </div>
  );
};

const SelectValue = ({ placeholder, children }) => {
  const { selectedValue } = useContext(SelectContext);
  
  if (!selectedValue && placeholder) {
    return <span className="text-gray-500">{placeholder}</span>;
  }
  
  return <span>{children || selectedValue}</span>;
};

export { Select, SelectContent, SelectItem, SelectTrigger, SelectValue };