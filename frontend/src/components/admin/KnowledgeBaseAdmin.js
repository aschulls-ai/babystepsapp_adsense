import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '../ui/card';
import { Button } from '../ui/button';
import { Input } from '../ui/input';
import { Label } from '../ui/label';
import { Textarea } from '../ui/textarea';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '../ui/select';
import { 
  Database, 
  Plus, 
  Search, 
  Download,
  Upload,
  BarChart3,
  RefreshCw
} from 'lucide-react';
import { toast } from 'sonner';
import knowledgeBaseService from '../../knowledgeBase';

const KnowledgeBaseAdmin = () => {
  const [selectedType, setSelectedType] = useState('ai_assistant');
  const [stats, setStats] = useState({});
  const [searchQuery, setSearchQuery] = useState('');
  const [searchResults, setSearchResults] = useState(null);
  const [showAddForm, setShowAddForm] = useState(false);
  const [newQuestion, setNewQuestion] = useState({
    category: '',
    age_range: '',
    question: '',
    answer: ''
  });

  const knowledgeBaseTypes = {
    ai_assistant: 'AI Assistant (Parenting)',
    meal_planner: 'Meal Planner',
    food_research: 'Food Research'
  };

  const categories = {
    ai_assistant: ['Feeding', 'Sleep', 'Development', 'Health', 'Safety', 'Behavior'],
    meal_planner: ['Feeding', 'Recipes', 'Nutrition', 'Safety'],
    food_research: ['Safety', 'Nutrition', 'Allergies', 'Introduction']
  };

  const ageRanges = [
    '0–3 months',
    '3–6 months', 
    '6–9 months',
    '9–12 months',
    '12+ months',
    '0–12 months',
    '6+ months'
  ];

  useEffect(() => {
    loadStats();
  }, []);

  const loadStats = () => {
    const allStats = knowledgeBaseService.getStats();
    setStats(allStats);
  };

  const handleSearch = () => {
    if (!searchQuery.trim()) return;
    
    const result = knowledgeBaseService.searchKnowledgeBase(searchQuery, selectedType, {
      babyAgeMonths: 12 // Default for testing
    });
    
    setSearchResults(result);
    
    if (result) {
      toast.success(`Found match: ${Math.round(result.similarity * 100)}% similarity`);
    } else {
      toast.info('No matches found in knowledge base');
    }
  };

  const handleAddQuestion = async () => {
    if (!newQuestion.question || !newQuestion.answer || !newQuestion.category) {
      toast.error('Please fill in all required fields');
      return;
    }

    const success = await knowledgeBaseService.addQuestionToKnowledgeBase(
      selectedType, 
      newQuestion.question, 
      newQuestion.answer,
      { category: newQuestion.category }
    );

    if (success) {
      toast.success('Question added successfully');
      setNewQuestion({ category: '', age_range: '', question: '', answer: '' });
      setShowAddForm(false);
      loadStats();
    } else {
      toast.error('Failed to add question');
    }
  };

  const downloadKnowledgeBase = async () => {
    try {
      const kb = knowledgeBaseService.knowledgeBases[selectedType];
      if (!kb) {
        toast.error('No knowledge base data to download');
        return;
      }

      const dataStr = JSON.stringify(kb, null, 2);
      const blob = new Blob([dataStr], { type: 'application/json' });
      const url = URL.createObjectURL(blob);
      
      const link = document.createElement('a');
      link.href = url;
      link.download = `${selectedType}_knowledge_base.json`;
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      URL.revokeObjectURL(url);
      
      toast.success('Knowledge base downloaded');
    } catch (error) {
      toast.error('Failed to download knowledge base');
    }
  };

  const uploadKnowledgeBase = (event) => {
    const file = event.target.files[0];
    if (!file) return;

    const reader = new FileReader();
    reader.onload = async (e) => {
      try {
        const jsonData = JSON.parse(e.target.result);
        
        if (!Array.isArray(jsonData)) {
          toast.error('Invalid JSON format. Expected an array of questions.');
          return;
        }

        const success = await knowledgeBaseService.updateKnowledgeBase(selectedType, jsonData);
        
        if (success) {
          toast.success(`Successfully uploaded ${jsonData.length} questions`);
          loadStats();
        } else {
          toast.error('Failed to update knowledge base');
        }
      } catch (error) {
        toast.error('Invalid JSON file');
      }
    };
    
    reader.readAsText(file);
    event.target.value = ''; // Reset input
  };

  const currentStats = stats[selectedType] || {};

  return (
    <div className="max-w-6xl mx-auto space-y-6 p-6">
      <div className="flex items-center justify-between">
        <h1 className="text-3xl font-bold text-gray-900">Knowledge Base Admin</h1>
        <Button onClick={loadStats} variant="outline" size="sm">
          <RefreshCw className="w-4 h-4 mr-2" />
          Refresh Stats
        </Button>
      </div>

      {/* Type Selector */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Database className="w-5 h-5" />
            Select Knowledge Base
          </CardTitle>
        </CardHeader>
        <CardContent>
          <Select value={selectedType} onValueChange={setSelectedType}>
            <SelectTrigger className="w-full">
              <SelectValue placeholder="Select knowledge base type" />
            </SelectTrigger>
            <SelectContent>
              {Object.entries(knowledgeBaseTypes).map(([key, label]) => (
                <SelectItem key={key} value={key}>
                  {label}
                </SelectItem>
              ))}
            </SelectContent>
          </Select>
        </CardContent>
      </Card>

      {/* Statistics */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <BarChart3 className="w-5 h-5" />
            Statistics - {knowledgeBaseTypes[selectedType]}
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <div className="text-center">
              <div className="text-2xl font-bold text-blue-600">
                {currentStats.questionCount || 0}
              </div>
              <div className="text-sm text-gray-500">Total Questions</div>
            </div>
            <div className="text-center">
              <div className="text-2xl font-bold text-green-600">
                {Object.keys(currentStats.categories || {}).length}
              </div>
              <div className="text-sm text-gray-500">Categories</div>
            </div>
            <div className="text-center">
              <div className="text-2xl font-bold text-purple-600">
                {currentStats.loaded ? '✓' : '✗'}
              </div>
              <div className="text-sm text-gray-500">Loaded</div>
            </div>
            <div className="text-center">
              <div className="text-2xl font-bold text-orange-600">
                {knowledgeBaseService.isReady(selectedType) ? '✓' : '✗'}
              </div>
              <div className="text-sm text-gray-500">Ready</div>
            </div>
          </div>
          
          {currentStats.categories && Object.keys(currentStats.categories).length > 0 && (
            <div className="mt-4">
              <h4 className="font-medium text-gray-700 mb-2">Category Breakdown:</h4>
              <div className="grid grid-cols-2 md:grid-cols-4 gap-2">
                {Object.entries(currentStats.categories).map(([category, count]) => (
                  <div key={category} className="text-sm">
                    <span className="font-medium">{category}:</span> {count}
                  </div>
                ))}
              </div>
            </div>
          )}
        </CardContent>
      </Card>

      {/* Search Testing */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Search className="w-5 h-5" />
            Test Search
          </CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="flex gap-3">
            <Input
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              placeholder="Enter a test query..."
              onKeyPress={(e) => e.key === 'Enter' && handleSearch()}
              className="flex-1"
            />
            <Button onClick={handleSearch}>
              <Search className="w-4 h-4 mr-2" />
              Search
            </Button>
          </div>

          {searchResults && (
            <div className="mt-4 p-4 bg-gray-50 rounded-lg">
              <div className="flex items-center justify-between mb-2">
                <span className="font-medium">Match Found:</span>
                <span className="text-sm bg-blue-100 text-blue-800 px-2 py-1 rounded">
                  {Math.round(searchResults.similarity * 100)}% similarity
                </span>
              </div>
              <div className="text-sm text-gray-600 mb-2">
                <strong>Question:</strong> {searchResults.question.question}
              </div>
              <div className="text-sm text-gray-600 mb-2">
                <strong>Category:</strong> {searchResults.question.category}
                {searchResults.question.age_range && (
                  <span className="ml-2">• <strong>Age:</strong> {searchResults.question.age_range}</span>
                )}
              </div>
              <div className="text-sm">
                <strong>Answer:</strong> 
                {Array.isArray(searchResults.question.answer) ? (
                  <div className="mt-2">
                    <span className="text-blue-600">{searchResults.question.answer.length} recipes available</span>
                    <div className="text-xs text-gray-500 mt-1">
                      Sample: {searchResults.question.answer[0]?.name || 'Recipe'}
                    </div>
                  </div>
                ) : (
                  <span className="ml-2">{searchResults.question.answer}</span>
                )}
              </div>
            </div>
          )}
        </CardContent>
      </Card>

      {/* File Operations */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* Upload */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Upload className="w-5 h-5" />
              Upload Knowledge Base
            </CardTitle>
          </CardHeader>
          <CardContent>
            <input
              type="file"
              accept=".json"
              onChange={uploadKnowledgeBase}
              className="block w-full text-sm text-gray-500
                file:mr-4 file:py-2 file:px-4
                file:rounded-full file:border-0
                file:text-sm file:font-semibold
                file:bg-blue-50 file:text-blue-700
                hover:file:bg-blue-100"
            />
            <p className="text-xs text-gray-500 mt-2">
              Upload a JSON file with questions in the correct format
            </p>
          </CardContent>
        </Card>

        {/* Download */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Download className="w-5 h-5" />
              Download Knowledge Base
            </CardTitle>
          </CardHeader>
          <CardContent>
            <Button onClick={downloadKnowledgeBase} className="w-full">
              <Download className="w-4 h-4 mr-2" />
              Download JSON File
            </Button>
            <p className="text-xs text-gray-500 mt-2">
              Download the current knowledge base as JSON
            </p>
          </CardContent>
        </Card>
      </div>

      {/* Add Question */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center justify-between">
            <div className="flex items-center gap-2">
              <Plus className="w-5 h-5" />
              Add New Question
            </div>
            <Button
              onClick={() => setShowAddForm(!showAddForm)}
              variant={showAddForm ? "secondary" : "default"}
            >
              {showAddForm ? 'Cancel' : 'Add Question'}
            </Button>
          </CardTitle>
        </CardHeader>
        {showAddForm && (
          <CardContent className="space-y-4">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <Label>Category *</Label>
                <Select 
                  value={newQuestion.category} 
                  onValueChange={(value) => setNewQuestion({...newQuestion, category: value})}
                >
                  <SelectTrigger>
                    <SelectValue placeholder="Select category" />
                  </SelectTrigger>
                  <SelectContent>
                    {(categories[selectedType] || []).map(cat => (
                      <SelectItem key={cat} value={cat}>{cat}</SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>
              <div>
                <Label>Age Range</Label>
                <Select 
                  value={newQuestion.age_range} 
                  onValueChange={(value) => setNewQuestion({...newQuestion, age_range: value})}
                >
                  <SelectTrigger>
                    <SelectValue placeholder="Select age range" />
                  </SelectTrigger>
                  <SelectContent>
                    {ageRanges.map(range => (
                      <SelectItem key={range} value={range}>{range}</SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>
            </div>
            
            <div>
              <Label>Question *</Label>
              <Input
                value={newQuestion.question}
                onChange={(e) => setNewQuestion({...newQuestion, question: e.target.value})}
                placeholder="Enter the question..."
              />
            </div>
            
            <div>
              <Label>Answer *</Label>
              <Textarea
                value={newQuestion.answer}
                onChange={(e) => setNewQuestion({...newQuestion, answer: e.target.value})}
                placeholder="Enter the answer..."
                rows={4}
              />
            </div>
            
            <Button onClick={handleAddQuestion} className="w-full">
              Add Question
            </Button>
          </CardContent>
        )}
      </Card>
    </div>
  );
};

export default KnowledgeBaseAdmin;