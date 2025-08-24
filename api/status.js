/**
 * Vercel API Function for Von Neu Status
 * Returns system status and chatroom information
 */

export default async function handler(req, res) {
  // Only allow GET requests
  if (req.method !== 'GET') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  try {
    // Check if API key is configured
    const apiKey = process.env.LLAMA_API_KEY;
    const apiConnected = !!apiKey;

    // Get query parameters for chatroom info
    const { currentRoom = 'general', totalRooms = 1, conversationLength = 0 } = req.query;

    const status = {
      api_connected: apiConnected,
      current_room: currentRoom,
      conversation_length: parseInt(conversationLength) || 0,
      total_rooms: parseInt(totalRooms) || 1,
      max_history_per_room: 75,
      model: 'meta/llama-3.1-70b-instruct',
      api_provider: 'NVIDIA',
      api_endpoint: 'https://integrate.api.nvidia.com/v1/chat/completions',
      memory_persistent: true,
      memory_file: 'Browser Local Storage',
      rate_limit_remaining: 40, // Default value for display
      timestamp: new Date().toISOString()
    };

    res.status(200).json(status);

  } catch (error) {
    console.error('Status API Error:', error);
    res.status(500).json({ 
      error: 'Internal server error',
      details: error.message
    });
  }
}