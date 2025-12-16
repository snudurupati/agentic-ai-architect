import asyncio
import os
import json
from openai import OpenAI
from mcp.client.sse import sse_client
from mcp.client.session import ClientSession
from dotenv import load_dotenv

# ============================================================================
# 1. SYSTEM PROMPT
# ============================================================================
SYSTEM_PROMPT = """
You are a helpful customer support assistant.

CRITICAL WORKFLOW FOR REFUNDS:
1. 🛑 **VERIFY FIRST:** If a user requests a refund or return, you MUST FIRST use `search_knowledge_base` to find the company's valid refund reasons and time windows.
2. 🕵️ **CHECK ELIGIBILITY:** Analyze the user's reason (e.g., "damaged", "changed mind") against the policy you just found.
3. ✅ **EXECUTE:** ONLY if the policy explicitly allows it, call `process_refund`.
4. ❌ **REJECT:** If the policy forbids it, explain why and DO NOT call `process_refund`.

You must follow this order: `search_knowledge_base` -> (Decision) -> `process_refund`.
"""

# Load environment variables from a .env file
load_dotenv()

async def run_agent():
    # Ensure we have an API key
    if not os.getenv("OPENAI_API_KEY"):
        print("❌ Error: OPENAI_API_KEY environment variable is not set.")
        return

    print("🔌 Connecting to MCP Server...")

    # Connect to the MCP Server
    async with sse_client("http://localhost:8000/sse") as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            
            # List available tools
            mcp_tools = await session.list_tools()
            print(f"✅ Connected! Found {len(mcp_tools.tools)} tools: {[t.name for t in mcp_tools.tools]}")

            # Initialize OpenAI Client
            client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
            
            # Start Chat Loop
            # We keep the history to maintain context
            messages = [{"role": "system", "content": SYSTEM_PROMPT}]

            while True:
                try:
                    user_query = input("\n👤 Query (or 'q' to quit): ")
                    if user_query.lower() in ['q', 'quit']:
                        break

                    # Add user message to history
                    messages.append({"role": "user", "content": user_query})

                    # ---------------------------------------------------------
                    # STEP A: Format Tools for OpenAI
                    # ---------------------------------------------------------
                    openai_tools = []
                    for tool in mcp_tools.tools:
                        openai_tools.append({
                            "type": "function",
                            "function": {
                                "name": tool.name,
                                "description": tool.description,
                                "parameters": tool.inputSchema  # MCP schema is compatible with OpenAI
                            }
                        })

                    # ---------------------------------------------------------
                    # STEP B: Call LLM (First Pass)
                    # ---------------------------------------------------------
                    response = client.chat.completions.create(
                        model="gpt-4o-mini", 
                        messages=messages,
                        tools=openai_tools,
                        tool_choice="auto"
                    )

                    # Get the message object
                    response_message = response.choices[0].message
                    tool_calls = response_message.tool_calls

                    # ---------------------------------------------------------
                    # STEP C: Handle Tool Use
                    # ---------------------------------------------------------
                    if tool_calls:
                        print(f"🤖 Agent decided to use {len(tool_calls)} tool(s)...")
                        
                        # OpenAI requires us to append the assistant's "thought" message first
                        messages.append(response_message)

                        for tool_call in tool_calls:
                            func_name = tool_call.function.name
                            func_args = json.loads(tool_call.function.arguments)
                            call_id = tool_call.id

                            print(f"   Executing: {func_name}({func_args})")

                            # Execute the tool on the MCP Server
                            result = await session.call_tool(func_name, arguments=func_args)
                            
                            # Extract text result
                            tool_output = result.content[0].text
                            print(f"   Result: {tool_output[:100]}...")

                            # Feed the result back to OpenAI
                            messages.append({
                                "role": "tool",
                                "tool_call_id": call_id,
                                "content": tool_output
                            })

                        # -----------------------------------------------------
                        # STEP D: Call LLM (Second Pass) - Get Final Answer
                        # -----------------------------------------------------
                        final_response = client.chat.completions.create(
                            model="gpt-4o-mini",
                            messages=messages
                        )
                        
                        final_text = final_response.choices[0].message.content
                        print(f"\n🤖 Answer: {final_text}")
                        messages.append({"role": "assistant", "content": final_text})

                    else:
                        # No tool used, just print response
                        final_text = response_message.content
                        print(f"\n🤖 Answer: {final_text}")
                        messages.append({"role": "assistant", "content": final_text})

                except Exception as e:
                    print(f"\n❌ Error in loop: {e}")

if __name__ == "__main__":
    asyncio.run(run_agent())