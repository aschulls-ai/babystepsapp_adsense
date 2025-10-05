import React, { useState, useEffect } from 'react';
import { Responsive, WidthProvider } from 'react-grid-layout';
import { Button } from './ui/button';
import { Card, CardContent, CardHeader, CardTitle } from './ui/card';
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger } from './ui/dialog';
import { Plus, Settings, Save, X } from 'lucide-react';
import { getWidgetComponent, DefaultWidgetConfigs } from './widgets/WidgetRegistry';
import { toast } from 'sonner';
import axios from 'axios';
import InContentAd from './ads/InContentAd';
import SidebarAd from './ads/SidebarAd';
import 'react-grid-layout/css/styles.css';
import 'react-resizable/css/styles.css';

const ResponsiveGridLayout = WidthProvider(Responsive);

const CustomizableDashboard = ({ currentBaby }) => {
  const [layout, setLayout] = useState([]);
  const [widgets, setWidgets] = useState([]);
  const [isEditing, setIsEditing] = useState(false);
  const [showAddWidget, setShowAddWidget] = useState(false);
  const [availableWidgets, setAvailableWidgets] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchDashboardLayout();
    fetchAvailableWidgets();
  }, []);

  const fetchDashboardLayout = async () => {
    try {
      const response = await axios.get('/dashboard/layout');
      const dashboardData = response.data;
      
      setWidgets(dashboardData.widgets || []);
      setLayout(dashboardData.widgets?.map(w => ({
        i: w.id,
        ...w.position
      })) || []);
    } catch (error) {
      console.error('Error fetching dashboard layout:', error);
      toast.error('Failed to load dashboard layout');
    } finally {
      setLoading(false);
    }
  };

  const fetchAvailableWidgets = async () => {
    try {
      const response = await axios.get('/dashboard/available-widgets');
      setAvailableWidgets(response.data.widgets);
    } catch (error) {
      console.error('Error fetching available widgets:', error);
    }
  };

  const handleLayoutChange = (newLayout) => {
    setLayout(newLayout);
    
    // Update widget positions
    const updatedWidgets = widgets.map(widget => {
      const layoutItem = newLayout.find(l => l.i === widget.id);
      if (layoutItem) {
        return {
          ...widget,
          position: {
            x: layoutItem.x,
            y: layoutItem.y,
            w: layoutItem.w,
            h: layoutItem.h
          }
        };
      }
      return widget;
    });
    
    setWidgets(updatedWidgets);
  };

  const saveDashboardLayout = async () => {
    try {
      await axios.put('/dashboard/layout', {
        widgets: widgets,
        layout_config: { cols: 12, rowHeight: 60 }
      });
      
      toast.success('Dashboard layout saved!');
      setIsEditing(false);
    } catch (error) {
      console.error('Error saving dashboard layout:', error);
      toast.error('Failed to save dashboard layout');
    }
  };

  const addWidget = async (widgetType) => {
    try {
      const widgetInfo = availableWidgets.find(w => w.type === widgetType);
      const config = DefaultWidgetConfigs[widgetType] || DefaultWidgetConfigs.baby_profile;
      
      // Find next available position
      const usedPositions = layout.map(l => ({ x: l.x, y: l.y }));
      let nextPosition = config.defaultPosition;
      
      // Simple collision detection - find empty spot
      while (usedPositions.some(p => p.x === nextPosition.x && p.y === nextPosition.y)) {
        nextPosition = { ...nextPosition, y: nextPosition.y + 1 };
      }

      const newWidget = {
        type: widgetType,
        title: widgetInfo?.name || 'New Widget',
        size: widgetInfo?.defaultSize || 'medium',
        position: nextPosition,
        config: { icon: widgetInfo?.icon || '📊' }
      };

      const response = await axios.post('/dashboard/widgets', newWidget);
      
      // Refresh dashboard
      await fetchDashboardLayout();
      setShowAddWidget(false);
      toast.success('Widget added successfully!');
    } catch (error) {
      console.error('Error adding widget:', error);
      toast.error('Failed to add widget');
    }
  };

  const removeWidget = async (widgetId) => {
    try {
      await axios.delete(`/dashboard/widgets/${widgetId}`);
      
      // Update local state
      setWidgets(widgets.filter(w => w.id !== widgetId));
      setLayout(layout.filter(l => l.i !== widgetId));
      
      toast.success('Widget removed');
    } catch (error) {
      console.error('Error removing widget:', error);
      toast.error('Failed to remove widget');
    }
  };

  const renderWidget = (widget) => {
    const WidgetComponent = getWidgetComponent(widget.type);
    
    if (!WidgetComponent) {
      return (
        <Card className="h-full">
          <CardContent className="p-4">
            <p className="text-center text-gray-500">Widget type '{widget.type}' not found</p>
          </CardContent>
        </Card>
      );
    }

    return (
      <WidgetComponent
        widget={widget}
        currentBaby={currentBaby}
        isEditing={isEditing}
        onRemove={removeWidget}
        onSettings={() => {}} // TODO: Implement widget settings
      />
    );
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center py-12">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-green-600"></div>
      </div>
    );
  }

  return (
    <div className="space-y-4">
      {/* Dashboard Controls */}
      <div className="flex items-center justify-between">
        <h2 className="text-2xl font-semibold">Dashboard</h2>
        <div className="flex gap-2">
          {isEditing ? (
            <>
              <Button onClick={saveDashboardLayout} size="sm">
                <Save className="h-4 w-4 mr-2" />
                Save Layout
              </Button>
              <Button 
                onClick={() => setIsEditing(false)} 
                variant="outline" 
                size="sm"
              >
                <X className="h-4 w-4 mr-2" />
                Cancel
              </Button>
            </>
          ) : (
            <>
              <Dialog open={showAddWidget} onOpenChange={setShowAddWidget}>
                <DialogTrigger asChild>
                  <Button size="sm">
                    <Plus className="h-4 w-4 mr-2" />
                    Add Widget
                  </Button>
                </DialogTrigger>
                <DialogContent className="max-w-2xl">
                  <DialogHeader>
                    <DialogTitle>Add Widget to Dashboard</DialogTitle>
                  </DialogHeader>
                  <div className="grid grid-cols-2 md:grid-cols-3 gap-4 max-h-96 overflow-y-auto">
                    {availableWidgets.map((widget) => (
                      <Card 
                        key={widget.type}
                        className="cursor-pointer hover:shadow-md transition-shadow"
                        onClick={() => addWidget(widget.type)}
                      >
                        <CardHeader className="pb-2">
                          <CardTitle className="text-sm flex items-center gap-2">
                            <span className="text-lg">{widget.icon}</span>
                            {widget.name}
                          </CardTitle>
                        </CardHeader>
                        <CardContent className="pt-0">
                          <p className="text-xs text-gray-600">{widget.description}</p>
                          <div className="mt-2">
                            <span className="text-xs bg-gray-100 px-2 py-1 rounded">
                              {widget.category}
                            </span>
                          </div>
                        </CardContent>
                      </Card>
                    ))}
                  </div>
                </DialogContent>
              </Dialog>
              
              <Button 
                onClick={() => setIsEditing(true)} 
                variant="outline" 
                size="sm"
              >
                <Settings className="h-4 w-4 mr-2" />
                Customize
              </Button>
            </>
          )}
        </div>
      </div>

      {/* Dashboard Grid with Ads */}
      {widgets.length > 0 ? (
        <div className="flex gap-6">
          {/* Main Dashboard Content */}
          <div className={`flex-1 ${isEditing ? 'ring-2 ring-blue-200 rounded-lg p-2' : ''}`}>
            <ResponsiveGridLayout
              className="layout"
              layouts={{ lg: layout }}
              breakpoints={{ lg: 1200, md: 996, sm: 768, xs: 480, xxs: 0 }}
              cols={{ lg: 12, md: 10, sm: 6, xs: 4, xxs: 2 }}
              rowHeight={60}
              onLayoutChange={handleLayoutChange}
              isDraggable={isEditing}
              isResizable={isEditing}
              margin={[16, 16]}
            >
              {widgets.map((widget, index) => (
                <div key={widget.id}>
                  {renderWidget(widget)}
                  {/* Add in-content ads after every 3rd widget */}
                  {(index + 1) % 3 === 0 && index < widgets.length - 1 && (
                    <div className="col-span-full mt-6">
                      <InContentAd />
                    </div>
                  )}
                </div>
              ))}
            </ResponsiveGridLayout>
          </div>
          
          {/* Sidebar Ad for Desktop */}
          <SidebarAd className="flex-shrink-0" />
        </div>
      ) : (
        <Card className="p-8 text-center">
          <CardContent>
            <div className="mb-4">
              <div className="w-16 h-16 bg-gray-100 rounded-full flex items-center justify-center mx-auto mb-4">
                <Plus className="h-8 w-8 text-gray-400" />
              </div>
              <h3 className="text-lg font-semibold mb-2">Customize Your Dashboard</h3>
              <p className="text-gray-600 mb-4">
                Add widgets to create your personalized Baby Steps dashboard with shortcuts to all your favorite features.
              </p>
              <Button onClick={() => setShowAddWidget(true)}>
                <Plus className="h-4 w-4 mr-2" />
                Add Your First Widget
              </Button>
            </div>
          </CardContent>
        </Card>
      )}

      {isEditing && (
        <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
          <p className="text-sm text-blue-800">
            <strong>Editing Mode:</strong> Drag widgets to rearrange them, resize by dragging the bottom-right corner, 
            or click the X button to remove widgets. Click "Save Layout" when you're done.
          </p>
        </div>
      )}
    </div>
  );
};

export default CustomizableDashboard;