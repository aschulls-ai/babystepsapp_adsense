import React from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '../ui/card';
import { Button } from '../ui/button';
import { X, Settings } from 'lucide-react';

const BaseWidget = ({ 
  widget, 
  children, 
  onRemove, 
  onSettings,
  isEditing = false,
  className = '' 
}) => {
  return (
    <Card className={`h-full ${className} ${isEditing ? 'ring-2 ring-blue-300' : ''}`}>
      <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
        <CardTitle className="text-sm font-medium flex items-center gap-2">
          <span>{widget.config.icon || '📊'}</span>
          {widget.title}
        </CardTitle>
        {isEditing && (
          <div className="flex gap-1">
            {onSettings && (
              <Button
                variant="ghost"
                size="sm"
                onClick={() => onSettings(widget)}
                className="h-6 w-6 p-0"
              >
                <Settings className="h-3 w-3" />
              </Button>
            )}
            <Button
              variant="ghost"
              size="sm"
              onClick={() => onRemove(widget.id)}
              className="h-6 w-6 p-0 text-red-500 hover:text-red-700"
            >
              <X className="h-3 w-3" />
            </Button>
          </div>
        )}
      </CardHeader>
      <CardContent className="h-[calc(100%-4rem)]">
        {children}
      </CardContent>
    </Card>
  );
};

export default BaseWidget;