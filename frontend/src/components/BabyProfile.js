import React, { useState } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from './ui/card';
import { Button } from './ui/button';
import { Input } from './ui/input';
import { Label } from './ui/label';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from './ui/select';
import { Calendar } from './ui/calendar';
import { Popover, PopoverContent, PopoverTrigger } from './ui/popover';
import { Baby, Calendar as CalendarIcon, Weight, Ruler, Plus, Heart } from 'lucide-react';
import { toast } from 'sonner';
import { format } from 'date-fns';

const BabyProfile = ({ currentBaby, onAddBaby }) => {
  const [showAddForm, setShowAddForm] = useState(!currentBaby);
  const [formData, setFormData] = useState({
    name: '',
    birth_date: new Date(),
    birth_weight: '',
    birth_length: '',
    gender: ''
  });
  const [showDatePicker, setShowDatePicker] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    try {
      const babyData = {
        ...formData,
        birth_weight: formData.birth_weight ? parseFloat(formData.birth_weight) : null,
        birth_length: formData.birth_length ? parseFloat(formData.birth_length) : null,
        gender: formData.gender || null
      };

      await onAddBaby(babyData);
      setShowAddForm(false);
      setFormData({
        name: '',
        birth_date: new Date(),
        birth_weight: '',
        birth_length: '',
        gender: ''
      });
    } catch (error) {
      console.error('Failed to add baby:', error);
    }
  };

  if (!currentBaby && !showAddForm) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <EmptyState onAddBaby={() => setShowAddForm(true)} />
      </div>
    );
  }

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
            className="bg-gradient-to-r from-rose-500 to-pink-500 hover:from-rose-600 hover:to-pink-600 text-white font-semibold py-2 px-6 rounded-xl shadow-lg hover:shadow-xl transition-all duration-300"
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
          <div className="bg-gradient-to-r from-rose-500 to-pink-500 p-6 text-white">
            <div className="flex items-center gap-6">
              <div className="w-20 h-20 bg-white/20 rounded-full flex items-center justify-center backdrop-blur-sm">
                <Baby className="w-10 h-10 text-white" />
              </div>
              <div className="flex-1">
                <h2 className="text-3xl font-bold font-display" data-testid="current-baby-name">
                  {currentBaby.name}
                </h2>
                <p className="text-rose-100 text-lg mt-1">
                  Born {format(new Date(currentBaby.birth_date), 'MMMM dd, yyyy')}
                </p>
                <div className="flex items-center gap-4 mt-3 text-sm">
                  <div className="flex items-center gap-1">
                    <CalendarIcon className="w-4 h-4" />
                    <span>{Math.floor((new Date() - new Date(currentBaby.birth_date)) / (1000 * 60 * 60 * 24))} days old</span>
                  </div>
                  {currentBaby.gender && (
                    <div className="flex items-center gap-1">
                      <Heart className="w-4 h-4" />
                      <span className="capitalize">{currentBaby.gender}</span>
                    </div>
                  )}
                </div>
              </div>
            </div>
          </div>

          <CardContent className="p-6">
            <div className="grid md:grid-cols-2 gap-6">
              {/* Birth Stats */}
              <div>
                <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center gap-2">
                  <Weight className="w-5 h-5 text-rose-500" />
                  Birth Information
                </h3>
                <div className="space-y-4">
                  <StatItem
                    label="Birth Weight"
                    value={currentBaby.birth_weight ? `${currentBaby.birth_weight} lbs` : 'Not recorded'}
                    icon={<Weight className="w-4 h-4 text-blue-500" />}
                  />
                  <StatItem
                    label="Birth Length"
                    value={currentBaby.birth_length ? `${currentBaby.birth_length} inches` : 'Not recorded'}
                    icon={<Ruler className="w-4 h-4 text-green-500" />}
                  />
                  <StatItem
                    label="Gender"
                    value={currentBaby.gender ? currentBaby.gender.charAt(0).toUpperCase() + currentBaby.gender.slice(1) : 'Not specified'}
                    icon={<Baby className="w-4 h-4 text-purple-500" />}
                  />
                </div>
              </div>

              {/* Growth Milestones Preview */}
              <div>
                <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center gap-2">
                  <Heart className="w-5 h-5 text-rose-500" />
                  Quick Stats
                </h3>
                <div className="space-y-4">
                  <div className="p-4 bg-gradient-to-r from-blue-50 to-cyan-50 rounded-lg border border-blue-100">
                    <div className="text-2xl font-bold text-blue-600 mb-1">
                      {Math.floor((new Date() - new Date(currentBaby.birth_date)) / (1000 * 60 * 60 * 24 * 7))}
                    </div>
                    <div className="text-sm text-blue-700 font-medium">Weeks Old</div>
                  </div>
                  <div className="p-4 bg-gradient-to-r from-green-50 to-emerald-50 rounded-lg border border-green-100">
                    <div className="text-2xl font-bold text-green-600 mb-1">
                      {Math.floor((new Date() - new Date(currentBaby.birth_date)) / (1000 * 60 * 60 * 24 * 30.44))}
                    </div>
                    <div className="text-sm text-green-700 font-medium">Months Old</div>
                  </div>
                  <div className="p-4 bg-gradient-to-r from-purple-50 to-violet-50 rounded-lg border border-purple-100">
                    <div className="text-lg font-bold text-purple-600 mb-1">
                      Growing Strong
                    </div>
                    <div className="text-sm text-purple-700 font-medium">Every day counts</div>
                  </div>
                </div>
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
              <Baby className="w-6 h-6 text-rose-500" />
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
                      className="w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:border-rose-400 focus:ring-2 focus:ring-rose-100 transition-all duration-200"
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
                          className="w-full justify-start text-left font-normal px-4 py-3 h-auto border-2 border-gray-200 rounded-xl hover:border-rose-400 focus:border-rose-400 focus:ring-2 focus:ring-rose-100"
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

                  <div className="space-y-2">
                    <Label htmlFor="gender" className="text-sm font-medium text-gray-700">
                      Gender
                    </Label>
                    <Select value={formData.gender} onValueChange={(value) => setFormData({...formData, gender: value})}>
                      <SelectTrigger 
                        className="w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:border-rose-400 focus:ring-2 focus:ring-rose-100"
                        data-testid="gender-selector"
                      >
                        <SelectValue placeholder="Select gender (optional)" />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="boy">Boy</SelectItem>
                        <SelectItem value="girl">Girl</SelectItem>
                        <SelectItem value="prefer-not-to-say">Prefer not to say</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>
                </div>

                {/* Birth Statistics */}
                <div className="space-y-4">
                  <div className="space-y-2">
                    <Label htmlFor="birth-weight" className="text-sm font-medium text-gray-700">
                      Birth Weight (lbs)
                    </Label>
                    <Input
                      id="birth-weight"
                      type="number"
                      step="0.1"
                      placeholder="e.g., 7.5"
                      value={formData.birth_weight}
                      onChange={(e) => setFormData({...formData, birth_weight: e.target.value})}
                      className="w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:border-rose-400 focus:ring-2 focus:ring-rose-100 transition-all duration-200"
                      data-testid="birth-weight-input"
                    />
                  </div>

                  <div className="space-y-2">
                    <Label htmlFor="birth-length" className="text-sm font-medium text-gray-700">
                      Birth Length (inches)
                    </Label>
                    <Input
                      id="birth-length"
                      type="number"
                      step="0.1"
                      placeholder="e.g., 20.5"
                      value={formData.birth_length}
                      onChange={(e) => setFormData({...formData, birth_length: e.target.value})}
                      className="w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:border-rose-400 focus:ring-2 focus:ring-rose-100 transition-all duration-200"
                      data-testid="birth-length-input"
                    />
                  </div>

                  <div className="p-4 bg-blue-50 rounded-lg border border-blue-200">
                    <p className="text-sm text-blue-700">
                      <strong>Tip:</strong> Birth measurements help track your baby's growth over time. You can add these details later if you don't have them now.
                    </p>
                  </div>
                </div>
              </div>

              {/* Form Actions */}
              <div className="flex flex-col sm:flex-row gap-3 pt-4">
                <Button
                  type="submit"
                  className="flex-1 bg-gradient-to-r from-rose-500 to-pink-500 hover:from-rose-600 hover:to-pink-600 text-white font-semibold py-3 px-6 rounded-xl shadow-lg hover:shadow-xl transition-all duration-300"
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
    </div>
  );
};

// Helper Components
const EmptyState = ({ onAddBaby }) => (
  <Card className="glass-strong border-0 max-w-md mx-auto text-center">
    <CardContent className="p-8">
      <div className="w-20 h-20 bg-gradient-to-br from-rose-400 to-pink-500 rounded-full flex items-center justify-center mx-auto mb-6">
        <Baby className="w-10 h-10 text-white" />
      </div>
      <h2 className="text-2xl font-bold font-display text-gray-900 mb-4">
        Add Your First Baby
      </h2>
      <p className="text-gray-600 mb-6">
        Create a profile for your little one to start tracking their growth, feeding, sleep, and milestones.
      </p>
      <Button
        onClick={onAddBaby}
        className="w-full bg-gradient-to-r from-rose-500 to-pink-500 hover:from-rose-600 hover:to-pink-600 text-white font-semibold py-3 rounded-xl shadow-lg hover:shadow-xl transition-all duration-300"
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

export default BabyProfile;