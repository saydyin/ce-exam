import type { FC, ChangeEvent } from 'react';
import { Settings } from '../types';
import { Button } from './common/Button';
import { Card } from './common/Card';

interface SettingsScreenProps {
  settings: Settings;
  onUpdateSettings: (newSettings: Partial<Settings>) => void;
  onBack: () => void;
}

export const SettingsScreen: FC<SettingsScreenProps> = ({ settings, onUpdateSettings, onBack }) => {
  const handleChange = (e: ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    const { name, value, type } = e.target;
    if (type === 'checkbox') {
        const { checked } = e.target as HTMLInputElement;
        onUpdateSettings({ [name]: checked });
    } else {
        onUpdateSettings({ [name]: value });
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900 flex items-center justify-center p-4">
      <Card className="max-w-lg w-full">
        <h1 className="text-2xl font-bold mb-6">Settings</h1>

        <div className="space-y-6">
          <div className="flex items-center justify-between">
            <label htmlFor="theme" className="font-semibold">Theme</label>
            <select
              id="theme"
              name="theme"
              value={settings.theme}
              onChange={handleChange}
              className="p-2 border rounded-md bg-white dark:bg-gray-700 border-gray-300 dark:border-gray-600 focus:ring-purple-500 focus:border-purple-500"
            >
              <option value="light">Light</option>
              <option value="dark">Dark</option>
            </select>
          </div>
          
          <div className="flex items-center justify-between">
            <label htmlFor="fontSize" className="font-semibold">Font Size</label>
            <select
              id="fontSize"
              name="fontSize"
              value={settings.fontSize}
              onChange={handleChange}
              className="p-2 border rounded-md bg-white dark:bg-gray-700 border-gray-300 dark:border-gray-600 focus:ring-purple-500 focus:border-purple-500"
            >
              <option value="small">Small</option>
              <option value="medium">Medium</option>
              <option value="large">Large</option>
            </select>
          </div>
          
          <div className="flex items-center justify-between">
            <label htmlFor="autoSave" className="font-semibold">Auto-save Progress</label>
            <label className="relative inline-flex items-center cursor-pointer">
              <input 
                type="checkbox" 
                id="autoSave"
                name="autoSave"
                checked={settings.autoSave}
                onChange={handleChange}
                className="sr-only peer"
              />
              <div className="w-11 h-6 bg-gray-200 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-purple-300 dark:peer-focus:ring-purple-800 rounded-full peer dark:bg-gray-700 peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all dark:border-gray-600 peer-checked:bg-purple-600"></div>
            </label>
          </div>
          
           {/* Add more settings as needed */}

        </div>

        <div className="mt-8 pt-6 border-t border-gray-200 dark:border-gray-700">
          <Button onClick={onBack} className="w-full">Back to Main Menu</Button>
        </div>
      </Card>
    </div>
  );
};
