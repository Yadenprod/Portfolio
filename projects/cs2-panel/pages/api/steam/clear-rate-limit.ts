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
    const { accountId } = req.body;

    if (!accountId) {
      return res.status(400).json({ error: 'Account ID is required' });
    }

    // Verify the account belongs to the current user
    const account = await Account.findOne({
      _id: accountId,
      user: session.user.id,
    });

    if (!account) {
      return res.status(404).json({ error: 'Account not found' });
    }

    // Check if account is rate-limited
    const wasRateLimited = steamManager.isRateLimited(accountId);
    
    // Clear the rate limit for this account
    steamManager.clearRateLimit(accountId);
    
    logger.info(`Rate limit cleared for account ${account.username} by user ${session.user.email}`);
    
    return res.status(200).json({
      success: true,
      wasRateLimited,
      message: wasRateLimited 
        ? `Rate limit for account ${account.username} has been cleared` 
        : `Account ${account.username} was not rate-limited`
    });
  } catch (error: any) {
    logger.error(`Error clearing rate limit: ${error.message}`);
    return res.status(500).json({
      success: false,
      error: `Server error: ${error.message}`
    });
  }
} 