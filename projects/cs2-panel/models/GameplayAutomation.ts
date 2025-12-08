import mongoose, { Schema, Document } from 'mongoose';

export interface IGameplayAutomation extends Document {
  _id: mongoose.Types.ObjectId;
  accountId: mongoose.Types.ObjectId;
  isActive: boolean;
  mapPreference: string;
  autoJoinDeathmatch: boolean;
  farmingHoursPerDay: number;
  autoReconnect: boolean;
  lastGameActivity: Date;
  experienceGained: number;
  currentLevel: number;
  nextCaseDropEstimate: Date;
  createdAt: Date;
  updatedAt: Date;
}

const GameplayAutomationSchema: Schema = new Schema(
  {
    accountId: { 
      type: mongoose.Schema.Types.ObjectId, 
      ref: 'Account', 
      required: true,
      unique: true 
    },
    isActive: { 
      type: Boolean, 
      default: false 
    },
    mapPreference: { 
      type: String, 
      enum: ['dust2', 'mirage', 'inferno', 'nuke', 'overpass', 'vertigo', 'ancient', 'anubis', 'any'],
      default: 'any'
    },
    autoJoinDeathmatch: { 
      type: Boolean, 
      default: true 
    },
    farmingHoursPerDay: { 
      type: Number, 
      default: 6,
      min: 1,
      max: 24 
    },
    autoReconnect: { 
      type: Boolean, 
      default: true 
    },
    lastGameActivity: { 
      type: Date 
    },
    experienceGained: {
      type: Number,
      default: 0
    },
    currentLevel: {
      type: Number,
      default: 1
    },
    nextCaseDropEstimate: {
      type: Date
    }
  },
  { timestamps: true }
);

export default mongoose.models.GameplayAutomation || 
  mongoose.model<IGameplayAutomation>('GameplayAutomation', GameplayAutomationSchema); 