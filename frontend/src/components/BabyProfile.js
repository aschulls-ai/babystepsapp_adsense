import React, { useState } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from './ui/card';
import { Button } from './ui/button';
import { Input } from './ui/input';
import { Label } from './ui/label';
import { Calendar } from './ui/calendar';
import { Popover, PopoverContent, PopoverTrigger } from './ui/popover';
import { Baby, Calendar as CalendarIcon, Plus, Heart } from 'lucide-react';
import { toast } from 'sonner';
import { format } from 'date-fns';
import PageAd from './ads/PageAd';

const BabyProfile = ({ currentBaby, onAddBaby, onUpdateBaby }) => {
  const [showAddForm, setShowAddForm] = useState(!currentBaby);
  const [showEditForm, setShowEditForm] = useState(false);
  const [formData, setFormData] = useState({
    name: '',
    birth_date: new Date()
  });
  const [editData, setEditData] = useState({
    name: currentBaby?.name || '',
    birth_date: currentBaby?.birth_date ? new Date(currentBaby.birth_date) : new Date()
  });
  const [showDatePicker, setShowDatePicker] = useState(false);
  const [showEditDatePicker, setShowEditDatePicker] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    try {
      await onAddBaby(formData);
      setShowAddForm(false);
      setFormData({
        name: '',
        birth_date: new Date()
      });
    } catch (error) {
      console.error('Failed to add baby:', error);
    }
  };

  const handleEdit = async (e) => {
    e.preventDefault();
    
    try {
      if (onUpdateBaby) {
        await onUpdateBaby(editData);
        setShowEditForm(false);
        toast.success('Baby profile updated successfully!');
      }
    } catch (error) {
      console.error('Failed to update baby:', error);
      toast.error('Failed to update baby profile');
    }
  };

  const startEdit = () => {
    setEditData({
      name: currentBaby?.name || '',
      birth_date: currentBaby?.birth_date ? new Date(currentBaby.birth_date) : new Date()
    });
    setShowEditForm(true);
  };

  if (!currentBaby && !showAddForm) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <EmptyState onAddBaby={() => setShowAddForm(true)} />
      </div>
    );
  }

  const babyAgeMonths = currentBaby ? Math.floor((new Date() - new Date(currentBaby.birth_date)) / (1000 * 60 * 60 * 24 * 30.44)) : 0;
  const babyAgeDays = currentBaby ? Math.floor((new Date() - new Date(currentBaby.birth_date)) / (1000 * 60 * 60 * 24)) : 0;

  return (
    <div className="max-w-4xl mx-auto space-y-6 fade-in">
      {/* Header */}
      <div className="flex flex-col lg:flex-row justify-between items-start lg:items-center gap-4">
        <div>
          <h1 className="text-4xl font-bold font-display text-gray-900" data-testid="baby-profile-title">
            Baby Profile
          </h1>
          <p className="text-lg text-gray-600 mt-2">
            {currentBaby ? `Manage ${currentBaby.name}'s information` : 'Add your little one\'s details'}
          </p>
        </div>
        {currentBaby && !showAddForm && (
          <Button
            onClick={() => setShowAddForm(true)}
            className="bg-gradient-to-r from-green-500 to-emerald-500 hover:from-green-600 hover:to-emerald-600 text-white font-semibold py-2 px-6 rounded-xl shadow-lg hover:shadow-xl transition-all duration-300"
            data-testid="add-another-baby-btn"
          >
            <Plus className="w-5 h-5 mr-2" />
            Add Another Baby
          </Button>
        )}
      </div>

      {/* Current Baby Profile */}
      {currentBaby && (
        <Card className="glass-strong border-0 overflow-hidden">
          <div className="bg-gradient-to-r from-green-500 to-emerald-500 p-6 text-white">
            <div className="flex items-center gap-6">
              <div className="w-20 h-20 bg-white/20 rounded-full flex items-center justify-center backdrop-blur-sm">
                <Baby className="w-10 h-10 text-white" />
              </div>
              <div className="flex-1">
                <h2 className="text-3xl font-bold font-display" data-testid="current-baby-name">
                  {currentBaby.name}
                </h2>
                <p className="text-green-100 text-lg mt-1">
                  Born {format(new Date(currentBaby.birth_date), 'MMMM dd, yyyy')}
                </p>
                <div className="flex items-center gap-4 mt-3 text-sm">
                  <div className="flex items-center gap-1">
                    <CalendarIcon className="w-4 h-4" />
                    <span>{babyAgeDays} days old</span>
                  </div>
                  <div className="flex items-center gap-1">
                    <Heart className="w-4 h-4" />
                    <span>{babyAgeMonths} months old</span>
                  </div>
                </div>
              </div>
              <div>
                <Button
                  onClick={startEdit}
                  variant="outline"
                  className="bg-white/20 border-white/30 text-white hover:bg-white/30 hover:border-white/40"
                >
                  Edit Profile
                </Button>
              </div>
            </div>
          </div>

          <CardContent className="p-6">
            <div className="grid md:grid-cols-2 gap-6">
              {/* Age Information */}
              <div>
                <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center gap-2">
                  <CalendarIcon className="w-5 h-5 text-green-500" />
                  Age Information
                </h3>
                <div className="space-y-4">
                  <StatItem
                    label="Days Old"
                    value={babyAgeDays}
                    icon={<CalendarIcon className="w-4 h-4 text-blue-500" />}
                  />
                  <StatItem
                    label="Months Old"
                    value={babyAgeMonths}
                    icon={<Baby className="w-4 h-4 text-green-500" />}
                  />
                  <StatItem
                    label="Weeks Old"
                    value={Math.floor(babyAgeDays / 7)}
                    icon={<Heart className="w-4 h-4 text-purple-500" />}
                  />
                </div>
              </div>

              {/* Feeding Stage */}
              <div>
                <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center gap-2">
                  <Heart className="w-5 h-5 text-green-500" />
                  Development Stage
                </h3>
                <FeedingStageInfo babyAgeMonths={babyAgeMonths} />
              </div>
            </div>
          </CardContent>
        </Card>
      )}

      {/* Add Baby Form */}
      {showAddForm && (
        <Card className="glass-strong border-0">
          <CardHeader>
            <CardTitle className="text-2xl font-semibold text-gray-900 flex items-center gap-2">
              <Baby className="w-6 h-6 text-green-500" />
              Add Baby Profile
            </CardTitle>
          </CardHeader>
          <CardContent>
            <form onSubmit={handleSubmit} className="space-y-6">
              <div className="grid md:grid-cols-2 gap-6">
                {/* Basic Information */}
                <div className="space-y-4">
                  <div className="space-y-2">
                    <Label htmlFor="baby-name" className="text-sm font-medium text-gray-700">
                      Baby's Name *
                    </Label>
                    <Input
                      id="baby-name"
                      type="text"
                      placeholder="Enter baby's name"
                      value={formData.name}
                      onChange={(e) => setFormData({...formData, name: e.target.value})}
                      required
                      className="w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:border-green-400 focus:ring-2 focus:ring-green-100 transition-all duration-200"
                      data-testid="baby-name-input"
                    />
                  </div>

                  <div className="space-y-2">
                    <Label htmlFor="birth-date" className="text-sm font-medium text-gray-700">
                      Birth Date *
                    </Label>
                    <Popover open={showDatePicker} onOpenChange={setShowDatePicker}>
                      <PopoverTrigger asChild>
                        <Button
                          variant="outline"
                          className="w-full justify-start text-left font-normal px-4 py-3 h-auto border-2 border-gray-200 rounded-xl hover:border-green-400 focus:border-green-400 focus:ring-2 focus:ring-green-100"
                          data-testid="birth-date-picker"
                        >
                          <CalendarIcon className="mr-2 h-4 w-4" />
                          {formData.birth_date ? format(formData.birth_date, 'PPP') : <span>Pick a date</span>}
                        </Button>
                      </PopoverTrigger>
                      <PopoverContent className="w-auto p-0" align="start">
                        <Calendar
                          mode="single"
                          selected={formData.birth_date}
                          onSelect={(date) => {
                            setFormData({...formData, birth_date: date});
                            setShowDatePicker(false);
                          }}
                          disabled={(date) => date > new Date() || date < new Date('1900-01-01')}
                          initialFocus
                        />
                      </PopoverContent>
                    </Popover>
                  </div>
                </div>

                {/* Safety Information */}
                <div className="space-y-4">
                  <div className="p-4 bg-green-50 rounded-lg border border-green-200">
                    <h4 className="text-sm font-medium text-green-800 mb-2">Why we need this information:</h4>
                    <ul className="text-xs text-green-700 space-y-1">
                      <li>• Provide age-appropriate food safety guidance</li>
                      <li>• Recommend suitable emergency training content</li>
                      <li>• Suggest developmentally appropriate meals</li>
                      <li>• Track important feeding milestones</li>
                    </ul>
                  </div>

                  <div className="disclaimer">
                    <p className="text-xs text-gray-600">
                      <span className="warning-text">⚠️ Privacy:</span> We only store your baby's name and birth date to provide personalized guidance. No other personal information is collected.
                    </p>
                  </div>
                </div>
              </div>

              {/* Form Actions */}
              <div className="flex flex-col sm:flex-row gap-3 pt-4">
                <Button
                  type="submit"
                  className="flex-1 bg-gradient-to-r from-green-500 to-emerald-500 hover:from-green-600 hover:to-emerald-600 text-white font-semibold py-3 px-6 rounded-xl shadow-lg hover:shadow-xl transition-all duration-300"
                  data-testid="save-baby-btn"
                >
                  <Baby className="w-5 h-5 mr-2" />
                  Save Baby Profile
                </Button>
                {currentBaby && (
                  <Button
                    type="button"
                    variant="outline"
                    onClick={() => setShowAddForm(false)}
                    className="flex-1 sm:flex-none px-6 py-3 border-2 border-gray-200 rounded-xl hover:bg-gray-50 transition-all duration-200"
                    data-testid="cancel-add-baby-btn"
                  >
                    Cancel
                  </Button>
                )}
              </div>
            </form>
          </CardContent>
        </Card>
      )}

      {/* Edit Baby Form */}
      {showEditForm && (
        <Card className="glass-strong border-0">
          <CardHeader>
            <CardTitle className="text-2xl font-bold font-display text-gray-900">
              Edit {currentBaby?.name}'s Profile
            </CardTitle>
          </CardHeader>
          <CardContent>
            <form onSubmit={handleEdit} className="space-y-6">
              <div className="grid md:grid-cols-2 gap-6">
                {/* Baby Name */}
                <div className="space-y-2">
                  <Label htmlFor="edit-name" className="text-sm font-medium text-gray-700">
                    Baby's Name *
                  </Label>
                  <Input
                    id="edit-name"
                    type="text"
                    value={editData.name}
                    onChange={(e) => setEditData({ ...editData, name: e.target.value })}
                    placeholder="Enter baby's name"
                    required
                    className="w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:ring-2 focus:ring-green-500 focus:border-transparent transition-all duration-200"
                  />
                </div>

                {/* Birth Date */}
                <div className="space-y-2">
                  <Label htmlFor="edit-birth-date" className="text-sm font-medium text-gray-700">
                    Birth Date *
                  </Label>
                  <Popover open={showEditDatePicker} onOpenChange={setShowEditDatePicker}>
                    <PopoverTrigger asChild>
                      <Button
                        variant="outline"
                        className="w-full px-4 py-3 border-2 border-gray-200 rounded-xl hover:bg-gray-50 transition-all duration-200 justify-start text-left font-normal"
                      >
                        <CalendarIcon className="mr-2 h-4 w-4" />
                        {editData.birth_date ? format(editData.birth_date, 'MMMM dd, yyyy') : 'Pick a date'}
                      </Button>
                    </PopoverTrigger>
                    <PopoverContent className="w-auto p-0" align="start">
                      <Calendar
                        mode="single"
                        selected={editData.birth_date}
                        onSelect={(date) => {
                          setEditData({ ...editData, birth_date: date });
                          setShowEditDatePicker(false);
                        }}
                        disabled={(date) => date > new Date() || date < new Date('1900-01-01')}
                        initialFocus
                      />
                    </PopoverContent>
                  </Popover>
                </div>
              </div>

              <div className="flex flex-col sm:flex-row gap-4 pt-6">
                <Button
                  type="submit"
                  className="flex-1 sm:flex-none bg-gradient-to-r from-green-500 to-emerald-500 hover:from-green-600 hover:to-emerald-600 text-white font-semibold py-3 px-8 rounded-xl shadow-lg hover:shadow-xl transition-all duration-300"
                >
                  Update Profile
                </Button>
                <Button
                  type="button"
                  variant="outline"
                  onClick={() => setShowEditForm(false)}
                  className="flex-1 sm:flex-none px-6 py-3 border-2 border-gray-200 rounded-xl hover:bg-gray-50 transition-all duration-200"
                >
                  Cancel
                </Button>
              </div>
            </form>
          </CardContent>
        </Card>
      )}

      {/* Page Ad */}
      <PageAd position="bottom" />
    </div>
  );
};

// Helper Components
const EmptyState = ({ onAddBaby }) => (
  <Card className="glass-strong border-0 max-w-md mx-auto text-center">
    <CardContent className="p-8">
      <div className="w-20 h-20 bg-gradient-to-br from-green-400 to-emerald-500 rounded-full flex items-center justify-center mx-auto mb-6">
        <Baby className="w-10 h-10 text-white" />
      </div>
      <h2 className="text-2xl font-bold font-display text-gray-900 mb-4">
        Add Your Baby
      </h2>
      <p className="text-gray-600 mb-6">
        Create a profile for your little one to get personalized nutrition guidance and safety information.
      </p>
      <Button
        onClick={onAddBaby}
        className="w-full bg-gradient-to-r from-green-500 to-emerald-500 hover:from-green-600 hover:to-emerald-600 text-white font-semibold py-3 rounded-xl shadow-lg hover:shadow-xl transition-all duration-300"
        data-testid="create-baby-profile-btn"
      >
        <Plus className="w-5 h-5 mr-2" />
        Create Baby Profile
      </Button>
    </CardContent>
  </Card>
);

const StatItem = ({ label, value, icon }) => (
  <div className="flex items-center gap-3 p-3 bg-gray-50 rounded-lg">
    <div className="p-2 bg-white rounded-lg shadow-sm">
      {icon}
    </div>
    <div>
      <div className="text-sm text-gray-500">{label}</div>
      <div className="font-medium text-gray-900">{value}</div>
    </div>
  </div>
);

const FeedingStageInfo = ({ babyAgeMonths }) => {
  let stage, description, stageColor;

  if (babyAgeMonths < 4) {
    stage = "Exclusive Milk";
    description = "Breast milk or formula only. No solid foods recommended.";
    stageColor = "age-0-6";
  } else if (babyAgeMonths < 6) {
    stage = "Pre-Solids";
    description = "Preparing for solid food introduction around 6 months.";
    stageColor = "age-0-6";
  } else if (babyAgeMonths < 12) {
    stage = "Food Introduction";
    description = "Introducing purees and soft finger foods gradually.";
    stageColor = "age-6-12";
  } else {
    stage = "Family Foods";
    description = "Transitioning to family meals with appropriate modifications.";
    stageColor = "age-12-plus";
  }

  return (
    <div className="space-y-4">
      <div className={`p-4 rounded-lg ${stageColor}`}>
        <h4 className="font-medium mb-1">{stage}</h4>
        <p className="text-sm">{description}</p>
      </div>
      
      <div className="p-3 bg-blue-50 rounded-lg border border-blue-200">
        <p className="text-xs text-blue-700">
          <strong>Remember:</strong> Every baby develops at their own pace. Always consult your pediatrician for personalized feeding guidance.
        </p>
      </div>
    </div>
  );
};

export default BabyProfile;