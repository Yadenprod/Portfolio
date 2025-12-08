import { NextApiRequest, NextApiResponse } from 'next';
import { unstable_getServerSession } from 'next-auth/next';
import { authOptions } from '../auth/[...nextauth]';
import dbConnect from '@/lib/dbConnect';
import Account from '@/models/Account';
import { logger } from '@/lib/logger';
import { steamManager } from '@/lib/steam';

export default async function handler(req: NextApiRequest, res: NextApiResponse) {
  // Only allow POST requests
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  try {
    // Check user authentication
    const session = await unstable_getServerSession(req, res, authOptions);
    if (!session) {
      return res.status(401).json({ error: 'Authentication required' });
    }

    await dbConnect();

    // Get account ID from request body
    const { accountId, steamGuardCode } = req.body;

    if (!accountId) {
      return res.status(400).json({ error: 'Account ID is required' });
    }

    // Find the account in the database
    const account = await Account.findOne({
      _id: accountId,
      user: session.user.id, // Verify the account belongs to the current user
    });

    if (!account) {
      return res.status(404).json({ error: 'Account not found' });
    }

    // If Steam Guard code is provided, save it to the database
    if (steamGuardCode) {
      logger.info(`Steam Guard code received for account ${account.username}: ${steamGuardCode}`);
      account.steamGuardCode = steamGuardCode;
      await account.save();
    }

    // Check if the account is already waiting for mobile confirmation
    if (steamManager.isWaitingForMobileConfirmation(accountId)) {
      return res.status(200).json({
        success: false,
        requiresMobileConfirmation: true,
        message: 'Already waiting for mobile confirmation. Please check your Steam Mobile app.'
      });
    }

    // Attempt to login with mobile confirmation enabled
    try {
      const status = await steamManager.loginAccount(account, {
        twoFactorCode: steamGuardCode,
        waitForMobileConfirmation: true
      });
      
      // If login is successful
      if (status.isLoggedIn) {
        // Update account status
        await Account.findByIdAndUpdate(accountId, {
          status: 'active',
          lastLogin: new Date()
        });
        
        return res.status(200).json({
          success: true,
          message: `Successfully logged into account ${account.username}`,
          status
        });
      } else if (status.requiresMobileConfirmation) {
        // If mobile confirmation is required
        return res.status(200).json({
          success: false,
          requiresMobileConfirmation: true,
          message: 'Please check your Steam Mobile app for confirmation',
          status
        });
      } else {
        // If login failed for other reasons
        return res.status(200).json({
          success: false,
          message: 'Failed to login to Steam account',
          status
        });
      }
    } catch (error: any) {
      logger.error(`Error logging into Steam for account ${account.username}: ${error.message}`);
      
      // Check for specific error types
      if (error.message && error.message.includes('mobile') || error.message.includes('подтверждение')) {
        return res.status(200).json({
          success: false,
          requiresMobileConfirmation: true,
          message: 'Please check your Steam Mobile app for confirmation'
        });
      } else if (error.message && error.message.includes('Вход уже выполняется')) {
        return res.status(409).json({
          success: false,
          message: 'Login already in progress, please wait for the previous request to complete'
        });
      }
      
      return res.status(500).json({
        success: false,
        error: `Error logging into Steam: ${error.message}`
      });
    }
  } catch (error: any) {
    logger.error(`API error during Steam login: ${error.message}`);
    return res.status(500).json({
      success: false,
      error: `Internal server error: ${error.message}`
    });
  }
} 