import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from './ui/card';
import { Button } from './ui/button';
import { Input } from './ui/input';
import { Badge } from './ui/badge';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from './ui/select';
import { 
  Search, 
  Filter, 
  Star, 
  AlertTriangle, 
  Leaf, 
  Shield, 
  Baby,
  Heart,
  CheckCircle,
  XCircle,
  Info,
  Clock,
  ExternalLink
} from 'lucide-react';
import InContentAd from './ads/InContentAd';
import PageAd from './ads/PageAd';

const FormulaComparison = ({ currentBaby }) => {
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedCondition, setSelectedCondition] = useState('all');
  const [selectedFormulas, setSelectedFormulas] = useState([]);

  // Scroll to top when component mounts
  useEffect(() => {
    window.scrollTo({ top: 0, behavior: 'instant' });
  }, []);

  // Comprehensive formula database
  const formulas = [
    {
      id: 1,
      name: 'Enfamil NeuroPro',
      brand: 'Enfamil',
      type: 'Infant Formula',
      price: '$34.99',
      rating: 4.5,
      reviews: 2847,
      organic: false,
      goodFor: ['healthy', 'brain-development'],
      keyIngredients: ['DHA', 'MFGM', 'Iron', 'Prebiotics'],
      hazardousIngredients: [],
      pros: ['Brain development support', 'Easy to digest', 'Closest to breast milk'],
      cons: ['More expensive', 'Contains palm oil'],
      description: 'Premium formula with brain-nourishing ingredients like MFGM and DHA.',
      ageRange: '0-12 months',
      website: 'https://www.enfamil.com/products/enfamil-neuropro-infant-formula/'
    },
    {
      id: 2,
      name: 'Similac Pro-Advance',
      brand: 'Similac',
      type: 'Infant Formula',
      price: '$32.99',
      rating: 4.3,
      reviews: 3156,
      organic: false,
      goodFor: ['healthy', 'immune-support'],
      keyIngredients: ['2\'-FL HMO', 'DHA', 'ARA', 'Iron', 'Prebiotics'],
      hazardousIngredients: [],
      pros: ['Immune system support', 'No artificial growth hormones', 'Easy mixing'],
      cons: ['Contains corn syrup', 'Some babies have gas issues'],
      description: 'Features 2\'-FL HMO, an immune-nourishing prebiotic like that found in breast milk.',
      ageRange: '0-12 months',
      website: 'https://www.similac.com/baby-formula/pro-advance.html'
    },
    {
      id: 3,
      name: 'Gerber Good Start GentlePro',
      brand: 'Gerber',
      type: 'Gentle Formula',
      price: '$28.99',
      rating: 4.2,
      reviews: 1923,
      organic: false,
      goodFor: ['sensitive-stomach', 'indigestion'],
      keyIngredients: ['Partially hydrolyzed proteins', 'DHA', '2\'-FL HMO', 'Probiotics'],
      hazardousIngredients: [],
      pros: ['Easier to digest', 'Reduces fussiness', 'Good for sensitive babies'],
      cons: ['Slightly thicker consistency', 'More expensive than basic formulas'],
      description: 'Gentle formula with partially broken down proteins for easier digestion.',
      ageRange: '0-12 months',
      website: 'https://www.gerber.com/gerber-good-start-gentlepro'
    },
    {
      id: 4,
      name: 'Earth\'s Best Organic',
      brand: 'Earth\'s Best',
      type: 'Organic Formula',
      price: '$39.99',
      rating: 4.4,
      reviews: 1456,
      organic: true,
      goodFor: ['healthy', 'organic-preference'],
      keyIngredients: ['Organic Lactose', 'DHA & ARA', 'Iron', 'Prebiotics', 'Organic ingredients'],
      hazardousIngredients: [],
      pros: ['USDA Organic certified', 'No artificial colors/flavors', 'Non-GMO'],
      cons: ['Most expensive option', 'Limited availability', 'Some mixing issues'],
      description: 'Certified organic formula made with organic lactose and no artificial ingredients.',
      ageRange: '0-12 months',
      website: 'https://www.earthsbest.com/en/products/formula'
    },
    {
      id: 5,
      name: 'Enfamil Gentlease',
      brand: 'Enfamil',
      type: 'Gentle Formula',
      price: '$33.99',
      rating: 4.6,
      reviews: 4231,
      organic: false,
      goodFor: ['indigestion', 'gas', 'fussiness'],
      keyIngredients: ['Partially hydrolyzed proteins', 'DHA', 'MFGM', 'Prebiotics'],
      hazardousIngredients: [],
      pros: ['Reduces fussiness in 24 hours', 'Easy to digest', 'Great for colicky babies'],
      cons: ['Thicker than regular formula', 'Slightly sweet taste'],
      description: 'Designed to reduce fussiness, gas, and crying in just 24 hours.',
      ageRange: '0-12 months',
      website: 'https://www.enfamil.com/products/enfamil-gentlease-infant-formula/'
    },
    {
      id: 6,
      name: 'Similac Alimentum',
      brand: 'Similac',
      type: 'Hypoallergenic',
      price: '$47.99',
      rating: 4.1,
      reviews: 892,
      organic: false,
      goodFor: ['allergies', 'lactose-intolerance', 'severe-sensitivity'],
      keyIngredients: ['Extensively hydrolyzed casein', 'DHA', 'ARA', 'MCT oil'],
      hazardousIngredients: [],
      pros: ['Hypoallergenic', 'For severe allergies', 'Fast relief for colic'],
      cons: ['Very expensive', 'Strong smell', 'Bitter taste'],
      description: 'Hypoallergenic formula for babies with severe food allergies and colic.',
      ageRange: '0-12 months',
      website: 'https://www.similac.com/baby-formula/alimentum.html'
    },
    {
      id: 7,
      name: 'Enfamil AR',
      brand: 'Enfamil',
      type: 'Anti-Reflux',
      price: '$35.99',
      rating: 4.3,
      reviews: 1167,
      organic: false,
      goodFor: ['acid-reflux', 'spit-up'],
      keyIngredients: ['Rice starch', 'DHA', 'MFGM', 'Iron', 'Prebiotics'],
      hazardousIngredients: [],
      pros: ['Reduces spit-up', 'Thickens in stomach', 'Clinically proven'],
      cons: ['Requires special nipple', 'More expensive', 'Thicker consistency'],
      description: 'Specially designed to reduce spit-up in babies with reflux issues.',
      ageRange: '0-12 months',
      website: 'https://www.enfamil.com/products/enfamil-ar-infant-formula/'
    },
    {
      id: 8,
      name: 'Similac Pro-Sensitive',
      brand: 'Similac',
      type: 'Lactose-Free',
      price: '$34.99',
      rating: 4.2,
      reviews: 2134,
      organic: false,
      goodFor: ['lactose-intolerance', 'sensitive-stomach'],
      keyIngredients: ['Corn syrup solids', '2\'-FL HMO', 'DHA', 'ARA', 'Iron'],
      hazardousIngredients: [],
      pros: ['Lactose-free', 'Easy digestion', 'Immune support'],
      cons: ['Contains corn syrup', 'Sweet taste', 'Some gas issues'],
      description: 'Lactose-free formula for babies with lactose sensitivity.',
      ageRange: '0-12 months',
      website: 'https://www.similac.com/baby-formula/pro-sensitive.html'
    },
    {
      id: 9,
      name: 'Kendamil Organic First Infant Milk',
      brand: 'Kendamil',
      type: 'Organic Formula',
      price: '$42.99',
      rating: 4.7,
      reviews: 1876,
      organic: true,
      goodFor: ['healthy', 'organic-preference', 'brain-development'],
      keyIngredients: ['Organic whole milk', 'DHA & ARA', 'HMOs', 'Organic lactose', 'No palm oil'],
      hazardousIngredients: [],
      pros: ['No palm oil', 'Made with whole milk', 'Organic certified', 'Closest to breast milk composition'],
      cons: ['Premium pricing', 'Limited availability in some areas'],
      description: 'Premium organic formula made with whole milk and free from palm oil, designed to be closest to breast milk.',
      ageRange: '0-6 months',
      website: 'https://www.kendamil.com/products/organic-first-infant-milk'
    },
    {
      id: 10,
      name: 'Kendamil Classic First Infant Milk',
      brand: 'Kendamil',
      type: 'Infant Formula',
      price: '$36.99',
      rating: 4.6,
      reviews: 2341,
      organic: false,
      goodFor: ['healthy', 'brain-development'],
      keyIngredients: ['Whole milk', 'DHA & ARA', 'HMOs', 'Lactose', 'No palm oil'],
      hazardousIngredients: [],
      pros: ['No palm oil', 'Made with whole milk', 'Great taste', 'Easy to digest'],
      cons: ['Slightly more expensive', 'Creamier texture may take adjustment'],
      description: 'Premium formula made with whole milk and naturally sourced nutrients, free from palm oil.',
      ageRange: '0-6 months',
      website: 'https://www.kendamil.com/products/classic-first-infant-milk'
    },
    {
      id: 11,
      name: 'Kendamil Comfort',
      brand: 'Kendamil',
      type: 'Gentle Formula',
      price: '$39.99',
      rating: 4.5,
      reviews: 1523,
      organic: false,
      goodFor: ['indigestion', 'gas', 'sensitive-stomach', 'fussiness'],
      keyIngredients: ['Partially hydrolyzed whey', 'Reduced lactose', 'DHA & ARA', 'Prebiotics', 'No palm oil'],
      hazardousIngredients: [],
      pros: ['Reduces colic and constipation', 'Easier digestion', 'No palm oil', 'Less gas and fussiness'],
      cons: ['More expensive than standard formula', 'Slight change in taste'],
      description: 'Specially formulated for babies with digestive sensitivities, featuring reduced lactose and partially hydrolyzed proteins.',
      ageRange: '0-12 months',
      website: 'https://www.kendamil.com/products/comfort-milk'
    },
    {
      id: 12,
      name: 'Kendamil Goat Milk Formula',
      brand: 'Kendamil',
      type: 'Goat Milk Formula',
      price: '$49.99',
      rating: 4.4,
      reviews: 892,
      organic: false,
      goodFor: ['sensitive-stomach', 'allergies', 'lactose-intolerance'],
      keyIngredients: ['Goat milk proteins', 'DHA & ARA', 'HMOs', 'Goat lactose', 'No palm oil'],
      hazardousIngredients: [],
      pros: ['Easier to digest than cow milk', 'Natural A2 proteins', 'No palm oil', 'Less allergenic'],
      cons: ['Most expensive option', 'Strong taste', 'Limited availability'],
      description: 'Made with goat milk proteins that are naturally easier to digest and less allergenic than cow milk proteins.',
      ageRange: '0-12 months',
      website: 'https://www.kendamil.com/products/goat-milk-formula'
    },
    {
      id: 13,
      name: 'Bobbie Organic Infant Formula',
      brand: 'Bobbie',
      type: 'Organic Formula',
      price: '$44.99',
      rating: 4.6,
      reviews: 1234,
      organic: true,
      goodFor: ['healthy', 'organic-preference', 'brain-development'],
      keyIngredients: ['Organic lactose', 'DHA & ARA', 'Iron', 'Prebiotics', 'No corn syrup'],
      hazardousIngredients: [],
      pros: ['USDA Organic', 'European-style formula', 'No corn syrup', 'Grass-fed milk'],
      cons: ['Subscription model', 'Premium price', 'Limited retail availability'],
      description: 'European-style organic formula made with grass-fed milk and organic lactose, no corn syrup.',
      ageRange: '0-12 months',
      website: 'https://www.hibobbie.com/'
    },
    {
      id: 14,
      name: 'Happy Baby Organic Formula',
      brand: 'Happy Baby',
      type: 'Organic Formula',
      price: '$37.99',
      rating: 4.3,
      reviews: 987,
      organic: true,
      goodFor: ['healthy', 'organic-preference'],
      keyIngredients: ['Organic lactose', 'DHA', 'ARA', 'Prebiotics', 'Iron'],
      hazardousIngredients: [],
      pros: ['USDA Organic', 'Affordable organic option', 'Easy to find'],
      cons: ['Contains maltodextrin', 'Some digestive issues reported'],
      description: 'Affordable USDA organic formula with essential nutrients for infant development.',
      ageRange: '0-12 months',
      website: 'https://www.happyfamilyorganics.com/products/baby-formula'
    },
    {
      id: 15,
      name: 'Gerber Extensive HA',
      brand: 'Gerber',
      type: 'Hypoallergenic',
      price: '$52.99',
      rating: 4.0,
      reviews: 456,
      organic: false,
      goodFor: ['allergies', 'severe-sensitivity', 'lactose-intolerance'],
      keyIngredients: ['100% whey protein hydrolysate', 'DHA', 'Probiotics', 'Lactose-free'],
      hazardousIngredients: [],
      pros: ['For severe allergies', 'Lactose-free', 'Probiotic support'],
      cons: ['Very expensive', 'Strong taste', 'Limited availability'],
      description: 'Extensively hydrolyzed hypoallergenic formula for babies with severe food allergies.',
      ageRange: '0-12 months',
      website: 'https://www.gerber.com/gerber-extensive-ha-infant-formula'
    },
    {
      id: 16,
      name: 'Nutramigen with Enflora LGG',
      brand: 'Enfamil',
      type: 'Hypoallergenic',
      price: '$49.99',
      rating: 4.2,
      reviews: 1567,
      organic: false,
      goodFor: ['allergies', 'colic', 'lactose-intolerance'],
      keyIngredients: ['Extensively hydrolyzed casein', 'LGG probiotic', 'DHA', 'ARA'],
      hazardousIngredients: [],
      pros: ['Manages colic fast', 'Proven allergy management', 'Contains LGG probiotic'],
      cons: ['Premium price', 'Strong smell', 'Bitter taste'],
      description: 'Hypoallergenic formula with LGG probiotic clinically proven to manage colic and allergies.',
      ageRange: '0-12 months',
      website: 'https://www.enfamil.com/products/nutramigen-infant-formula/'
    },
    {
      id: 17,
      name: 'Similac Spit-Up',
      brand: 'Similac',
      type: 'Anti-Reflux',
      price: '$33.99',
      rating: 4.4,
      reviews: 2103,
      organic: false,
      goodFor: ['acid-reflux', 'spit-up'],
      keyIngredients: ['Rice starch', '2\'-FL HMO', 'DHA', 'ARA', 'Iron'],
      hazardousIngredients: [],
      pros: ['Reduces spit-up frequency', 'Thickens in stomach', 'Immune support'],
      cons: ['Requires special nipple', 'Thicker texture'],
      description: 'Thickened formula with rice starch clinically shown to reduce spit-up by over 50%.',
      ageRange: '0-12 months',
      website: 'https://www.similac.com/baby-formula/similac-for-spit-up.html'
    },
    {
      id: 18,
      name: 'Enfamil Reguline',
      brand: 'Enfamil',
      type: 'Digestive Support',
      price: '$35.99',
      rating: 4.1,
      reviews: 876,
      organic: false,
      goodFor: ['constipation', 'indigestion'],
      keyIngredients: ['Prebiotics', 'DHA', 'Iron', 'Dual probiotics'],
      hazardousIngredients: [],
      pros: ['Eases constipation', 'Supports regularity', 'Dual probiotic blend'],
      cons: ['May cause loose stools initially', 'More expensive'],
      description: 'Designed to promote comfortable bowel movements and ease constipation in infants.',
      ageRange: '0-12 months',
      website: 'https://www.enfamil.com/products/enfamil-reguline-infant-formula/'
    },
    {
      id: 19,
      name: 'Similac Total Comfort',
      brand: 'Similac',
      type: 'Gentle Formula',
      price: '$36.99',
      rating: 4.3,
      reviews: 1890,
      organic: false,
      goodFor: ['gas', 'fussiness', 'sensitive-stomach'],
      keyIngredients: ['Partially broken down whey protein', '2\'-FL HMO', 'DHA', 'Reduced lactose'],
      hazardousIngredients: [],
      pros: ['Gentle on tummies', 'Reduced lactose', 'Easy to digest'],
      cons: ['Sweet taste', 'More expensive than regular'],
      description: 'Gentle, easy-to-digest formula for babies with sensitive tummies.',
      ageRange: '0-12 months',
      website: 'https://www.similac.com/baby-formula/total-comfort.html'
    },
    {
      id: 20,
      name: 'Holle Organic Infant Formula',
      brand: 'Holle',
      type: 'Organic Formula',
      price: '$45.99',
      rating: 4.5,
      reviews: 1345,
      organic: true,
      goodFor: ['healthy', 'organic-preference'],
      keyIngredients: ['Organic milk', 'Organic lactose', 'DHA', 'ARA', 'Omega-3 & 6'],
      hazardousIngredients: [],
      pros: ['Demeter certified biodynamic', 'European formula', 'No added sugar', 'High quality'],
      cons: ['Expensive', 'Must be imported', 'Availability issues'],
      description: 'Premium European organic formula with biodynamic certification and high-quality ingredients.',
      ageRange: '0-6 months',
      website: 'https://www.holle.ch/en/baby-food/infant-formula/'
    },
    {
      id: 21,
      name: 'HiPP Organic Combiotik',
      brand: 'HiPP',
      type: 'Organic Formula',
      price: '$43.99',
      rating: 4.6,
      reviews: 2456,
      organic: true,
      goodFor: ['healthy', 'organic-preference', 'immune-support'],
      keyIngredients: ['Organic milk', 'Prebiotics', 'Probiotics', 'DHA', 'ARA', 'Omega-3'],
      hazardousIngredients: [],
      pros: ['European certified organic', 'Prebiotic & probiotic blend', 'No corn syrup', 'High standards'],
      cons: ['Import required', 'Premium price', 'Limited US availability'],
      description: 'German organic formula with prebiotics and probiotics for optimal digestive health.',
      ageRange: '0-6 months',
      website: 'https://www.hipp.com/en/baby-food/infant-formula/'
    },
    {
      id: 22,
      name: 'Baby\'s Only Organic Dairy',
      brand: 'Baby\'s Only',
      type: 'Organic Toddler Formula',
      price: '$29.99',
      rating: 4.2,
      reviews: 789,
      organic: true,
      goodFor: ['healthy', 'organic-preference'],
      keyIngredients: ['Organic milk', 'DHA', 'ARA', 'Iron', 'Prebiotics'],
      hazardousIngredients: [],
      pros: ['USDA Organic', 'Affordable', 'For toddlers', 'No corn syrup solids'],
      cons: ['Not for infants under 12 months', 'Lower calorie density'],
      description: 'Organic toddler formula for babies 12+ months as a supplement to solid foods.',
      ageRange: '12+ months',
      website: 'https://www.naturesone.com/product/babys-only-organic-dairy-toddler-formula/'
    },
    {
      id: 23,
      name: 'Similac 360 Total Care',
      brand: 'Similac',
      type: 'Infant Formula',
      price: '$38.99',
      rating: 4.5,
      reviews: 1678,
      organic: false,
      goodFor: ['healthy', 'brain-development', 'immune-support'],
      keyIngredients: ['5 HMOs', 'DHA', 'Lutein', 'Vitamin E', 'Prebiotics'],
      hazardousIngredients: [],
      pros: ['5 HMOs for immune support', 'Brain and eye development', 'Closest to breast milk'],
      cons: ['Premium price', 'Newer formula with limited reviews'],
      description: 'Advanced formula with 5 HMOs to support immune defense like breast milk.',
      ageRange: '0-12 months',
      website: 'https://www.similac.com/baby-formula/similac-360-total-care.html'
    },
    {
      id: 24,
      name: 'Enfamil Enspire',
      brand: 'Enfamil',
      type: 'Premium Infant Formula',
      price: '$46.99',
      rating: 4.7,
      reviews: 2341,
      organic: false,
      goodFor: ['healthy', 'brain-development', 'immune-support'],
      keyIngredients: ['MFGM', 'Lactoferrin', 'DHA', 'Prebiotics', 'Immune proteins'],
      hazardousIngredients: [],
      pros: ['Contains lactoferrin', 'MFGM for brain development', 'Closest to breast milk', 'Premium ingredients'],
      cons: ['Most expensive Enfamil', 'Can be hard to find'],
      description: 'Enfamil\'s closest formula to breast milk with lactoferrin and MFGM for immune and brain support.',
      ageRange: '0-12 months',
      website: 'https://www.enfamil.com/products/enfamil-enspire-infant-formula/'
    },
    {
      id: 25,
      name: 'Parent\'s Choice Organic',
      brand: 'Parent\'s Choice',
      type: 'Organic Formula',
      price: '$24.99',
      rating: 3.9,
      reviews: 1456,
      organic: true,
      goodFor: ['healthy', 'organic-preference', 'budget'],
      keyIngredients: ['Organic lactose', 'DHA', 'ARA', 'Iron', 'Prebiotics'],
      hazardousIngredients: [],
      pros: ['Most affordable organic', 'USDA certified', 'Walmart exclusive', 'Good value'],
      cons: ['Only at Walmart', 'Basic formulation', 'Some mixing issues'],
      description: 'Budget-friendly organic formula option available exclusively at Walmart stores.',
      ageRange: '0-12 months',
      website: 'https://www.walmart.com/browse/baby/parents-choice-baby-formula/'
    }
  ];

  const conditions = [
    { value: 'all', label: 'All Conditions' },
    { value: 'healthy', label: 'Healthy Baby' },
    { value: 'indigestion', label: 'Indigestion' },
    { value: 'acid-reflux', label: 'Acid Reflux' },
    { value: 'lactose-intolerance', label: 'Lactose Intolerance' },
    { value: 'sensitive-stomach', label: 'Sensitive Stomach' },
    { value: 'allergies', label: 'Allergies' },
    { value: 'gas', label: 'Gas Issues' },
    { value: 'organic-preference', label: 'Organic Preference' }
  ];

  const filteredFormulas = formulas.filter(formula => {
    const matchesSearch = formula.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         formula.brand.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         formula.type.toLowerCase().includes(searchTerm.toLowerCase());
    
    const matchesCondition = selectedCondition === 'all' || 
                            formula.goodFor.includes(selectedCondition);
    
    return matchesSearch && matchesCondition;
  });

  const toggleFormulaSelection = (formulaId) => {
    setSelectedFormulas(prev => 
      prev.includes(formulaId) 
        ? prev.filter(id => id !== formulaId)
        : prev.length < 3 ? [...prev, formulaId] : prev
    );
  };

  const selectedFormulaData = formulas.filter(f => selectedFormulas.includes(f.id));

  const getRatingStars = (rating) => {
    return Array.from({ length: 5 }, (_, i) => (
      <Star 
        key={i} 
        className={`w-4 h-4 ${i < rating ? 'text-yellow-400 fill-current' : 'text-gray-300'}`} 
      />
    ));
  };

  const getConditionBadge = (goodFor) => {
    const colors = {
      'healthy': 'bg-green-100 text-green-800',
      'indigestion': 'bg-orange-100 text-orange-800',
      'acid-reflux': 'bg-red-100 text-red-800',
      'lactose-intolerance': 'bg-blue-100 text-blue-800',
      'sensitive-stomach': 'bg-purple-100 text-purple-800',
      'allergies': 'bg-pink-100 text-pink-800',
      'gas': 'bg-yellow-100 text-yellow-800',
      'organic-preference': 'bg-green-100 text-green-800'
    };

    return goodFor.map((condition, index) => (
      <Badge key={index} className={`${colors[condition] || 'bg-gray-100 text-gray-800'} text-xs`}>
        {condition.replace('-', ' ').replace(/\b\w/g, l => l.toUpperCase())}
      </Badge>
    ));
  };

  return (
    <div className="container mx-auto px-4 py-6 max-w-7xl">
      {/* Header */}
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-2">Baby Formula Comparison</h1>
        <p className="text-lg text-gray-600 dark:text-gray-300">
          Compare popular baby formulas to find the best choice for {currentBaby?.name || 'your baby'}
        </p>
      </div>

      {/* Search and Filter */}
      <Card className="mb-8">
        <CardContent className="p-6">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="relative">
              <Search className="absolute left-3 top-3 h-4 w-4 text-gray-400 dark:text-gray-500" />
              <Input
                placeholder="Search formulas by name, brand, or type..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="pl-10 bg-white dark:bg-gray-800 text-gray-900 dark:text-white border-gray-300 dark:border-gray-600"
              />
              <p className="text-xs text-gray-500 dark:text-gray-400 mt-2 flex items-center">
                <Clock className="w-3 h-3 mr-1" />
                Response may take up to a minute due to AI processing and customizing for {currentBaby?.name || 'your baby'}
              </p>
            </div>
            <Select value={selectedCondition} onValueChange={setSelectedCondition}>
              <SelectTrigger className="bg-white dark:bg-gray-800 text-gray-900 dark:text-white border-gray-300 dark:border-gray-600">
                <Filter className="h-4 w-4 mr-2" />
                <SelectValue placeholder="Filter by condition" />
              </SelectTrigger>
              <SelectContent>
                {conditions.map((condition) => (
                  <SelectItem key={condition.value} value={condition.value}>
                    {condition.label}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
          </div>
        </CardContent>
      </Card>

      {/* Comparison Table */}
      {selectedFormulas.length > 0 && (
        <Card className="mb-8">
          <CardHeader>
            <CardTitle className="flex items-center">
              <Baby className="h-5 w-5 mr-2 text-blue-600" />
              Formula Comparison ({selectedFormulas.length}/3)
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="overflow-x-auto">
              <table className="w-full">
                <thead>
                  <tr className="border-b">
                    <th className="text-left p-4">Feature</th>
                    {selectedFormulaData.map(formula => (
                      <th key={formula.id} className="text-left p-4 min-w-[200px]">
                        <div className="flex items-center justify-between">
                          <span>{formula.name}</span>
                          <Button
                            variant="ghost"
                            size="sm"
                            onClick={() => toggleFormulaSelection(formula.id)}
                          >
                            <XCircle className="h-4 w-4" />
                          </Button>
                        </div>
                      </th>
                    ))}
                  </tr>
                </thead>
                <tbody>
                  <tr className="border-b">
                    <td className="p-4 font-medium">Price</td>
                    {selectedFormulaData.map(formula => (
                      <td key={formula.id} className="p-4">{formula.price}</td>
                    ))}
                  </tr>
                  <tr className="border-b">
                    <td className="p-4 font-medium">Rating</td>
                    {selectedFormulaData.map(formula => (
                      <td key={formula.id} className="p-4">
                        <div className="flex items-center space-x-2">
                          <div className="flex">{getRatingStars(formula.rating)}</div>
                          <span className="text-sm text-gray-600 dark:text-gray-300">({formula.reviews})</span>
                        </div>
                      </td>
                    ))}
                  </tr>
                  <tr className="border-b">
                    <td className="p-4 font-medium">Organic</td>
                    {selectedFormulaData.map(formula => (
                      <td key={formula.id} className="p-4">
                        {formula.organic ? (
                          <Badge className="bg-green-100 text-green-800">
                            <Leaf className="h-3 w-3 mr-1" />
                            Organic
                          </Badge>
                        ) : (
                          <span className="text-gray-500">Non-organic</span>
                        )}
                      </td>
                    ))}
                  </tr>
                  <tr className="border-b">
                    <td className="p-4 font-medium">Good For</td>
                    {selectedFormulaData.map(formula => (
                      <td key={formula.id} className="p-4">
                        <div className="flex flex-wrap gap-1">
                          {getConditionBadge(formula.goodFor)}
                        </div>
                      </td>
                    ))}
                  </tr>
                  <tr className="border-b">
                    <td className="p-4 font-medium">Key Ingredients</td>
                    {selectedFormulaData.map(formula => (
                      <td key={formula.id} className="p-4">
                        <ul className="text-sm list-disc list-inside">
                          {formula.keyIngredients.slice(0, 3).map((ingredient, idx) => (
                            <li key={idx}>{ingredient}</li>
                          ))}
                        </ul>
                      </td>
                    ))}
                  </tr>
                </tbody>
              </table>
            </div>
          </CardContent>
        </Card>
      )}

      {/* Formula Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-8">
        {filteredFormulas.map((formula) => (
          <Card key={formula.id} className="hover:shadow-lg transition-shadow">
            <CardHeader>
              <div className="flex items-start justify-between">
                <div>
                  <CardTitle className="text-lg">{formula.name}</CardTitle>
                  <p className="text-sm text-gray-600 dark:text-gray-300">{formula.brand} • {formula.type}</p>
                </div>
                <div className="text-right">
                  <p className="text-lg font-bold text-green-600">{formula.price}</p>
                  {formula.organic && (
                    <Badge className="bg-green-100 text-green-800 mt-1">
                      <Leaf className="h-3 w-3 mr-1" />
                      Organic
                    </Badge>
                  )}
                </div>
              </div>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {/* Rating */}
                <div className="flex items-center space-x-2">
                  <div className="flex">{getRatingStars(formula.rating)}</div>
                  <span className="text-sm text-gray-600 dark:text-gray-300">
                    {formula.rating} ({formula.reviews} reviews)
                  </span>
                </div>

                {/* Description */}
                <p className="text-sm text-gray-700 dark:text-gray-200">{formula.description}</p>

                {/* Brand Website Link */}
                {formula.website && (
                  <a
                    href={formula.website}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="inline-flex items-center gap-1 text-xs text-blue-600 hover:text-blue-800 hover:underline"
                  >
                    <ExternalLink className="h-3 w-3" />
                    Visit {formula.brand} Website
                  </a>
                )}

                {/* Good For */}
                <div>
                  <h4 className="text-sm font-semibold mb-2 flex items-center">
                    <Heart className="h-4 w-4 mr-1 text-red-500" />
                    Good For:
                  </h4>
                  <div className="flex flex-wrap gap-1">
                    {getConditionBadge(formula.goodFor)}
                  </div>
                </div>

                {/* Key Ingredients */}
                <div>
                  <h4 className="text-sm font-semibold mb-2 flex items-center">
                    <Shield className="h-4 w-4 mr-1 text-blue-500" />
                    Key Ingredients:
                  </h4>
                  <ul className="text-xs text-gray-600 list-disc list-inside">
                    {formula.keyIngredients.slice(0, 4).map((ingredient, idx) => (
                      <li key={idx}>{ingredient}</li>
                    ))}
                  </ul>
                </div>

                {/* Pros & Cons */}
                <div className="grid grid-cols-2 gap-2 text-xs">
                  <div>
                    <h5 className="font-semibold text-green-700 mb-1">Pros:</h5>
                    <ul className="text-green-600 space-y-1">
                      {formula.pros.slice(0, 2).map((pro, idx) => (
                        <li key={idx} className="flex items-start">
                          <CheckCircle className="h-3 w-3 mr-1 mt-0.5 flex-shrink-0" />
                          {pro}
                        </li>
                      ))}
                    </ul>
                  </div>
                  <div>
                    <h5 className="font-semibold text-red-700 mb-1">Cons:</h5>
                    <ul className="text-red-600 space-y-1">
                      {formula.cons.slice(0, 2).map((con, idx) => (
                        <li key={idx} className="flex items-start">
                          <XCircle className="h-3 w-3 mr-1 mt-0.5 flex-shrink-0" />
                          {con}
                        </li>
                      ))}
                    </ul>
                  </div>
                </div>

                {/* Action Button */}
                <Button
                  onClick={() => toggleFormulaSelection(formula.id)}
                  className={`w-full mt-4 ${
                    selectedFormulas.includes(formula.id)
                      ? 'bg-green-600 hover:bg-green-700'
                      : 'bg-blue-600 hover:bg-blue-700'
                  }`}
                  disabled={!selectedFormulas.includes(formula.id) && selectedFormulas.length >= 3}
                >
                  {selectedFormulas.includes(formula.id) 
                    ? 'Remove from Comparison' 
                    : selectedFormulas.length >= 3 
                      ? 'Max 3 Formulas' 
                      : 'Add to Comparison'
                  }
                </Button>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>

      {/* In-content Ad */}
      <InContentAd />

      {/* Important Safety Notice */}
      <Card className="bg-yellow-50 border-yellow-200">
        <CardContent className="p-6">
          <div className="flex items-start space-x-3">
            <AlertTriangle className="h-5 w-5 text-yellow-600 mt-1 flex-shrink-0" />
            <div>
              <h3 className="font-semibold text-yellow-800 mb-2">Important Safety Notice</h3>
              <div className="text-sm text-yellow-700 space-y-2">
                <p>• Always consult your pediatrician before choosing or switching formulas</p>
                <p>• Follow preparation instructions exactly as directed on the package</p>
                <p>• Never dilute or concentrate formula beyond recommended ratios</p>
                <p>• This comparison is for educational purposes only and not medical advice</p>
                <p>• If your baby shows signs of allergic reactions, contact your doctor immediately</p>
              </div>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Page Ad */}
      <PageAd position="bottom" adUnitKey="banner_formula" />
    </div>
  );
};

export default FormulaComparison;