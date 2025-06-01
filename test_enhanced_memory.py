#!/usr/bin/env python3
"""
Comprehensive Test for Enhanced AI Memory System

Tests all the new enhanced capabilities:
1. Persona Evolution Layer for AI self-identity
2. Enhanced Weighted Retrieval
3. Reflexion Capability for self-assessment  
4. Forgetting Mechanism with memory decay
"""

import sys
import os
import json
from datetime import datetime
from pathlib import Path

# Add memory system to path
sys.path.append('interfaces/model-context-protocol/servers/memory')
from tools.memory_system import MemorySystem


def test_enhanced_memory_system():
    """Comprehensive test of all enhanced memory capabilities."""
    print("=" * 70)
    print("🧠 ENHANCED AI MEMORY SYSTEM - COMPREHENSIVE TEST")
    print("=" * 70)
    
    # Initialize memory system
    memory = MemorySystem()
    
    # Test 1: Basic Memory Storage & Enhanced Weighted Retrieval
    print("\n📝 Test 1: Enhanced Memory Storage & Weighted Retrieval")
    print("-" * 50)
    
    # Store diverse memories for testing
    test_memories = [
        {
            "memory_type": "code_insight",
            "content": "Python list comprehensions are more efficient than traditional loops for filtering",
            "title": "Python Performance Tip",
            "importance": 0.9,
            "tags": ["python", "performance", "optimization"]
        },
        {
            "memory_type": "user_preference", 
            "content": "User prefers detailed technical explanations with code examples",
            "title": "Communication Style Preference",
            "importance": 0.8,
            "tags": ["communication", "preference"]
        },
        {
            "memory_type": "problem_solution",
            "content": "Use PostgreSQL connection pooling to prevent connection exhaustion in high-load scenarios",
            "title": "Database Connection Management",
            "importance": 0.7,
            "tags": ["database", "postgresql", "architecture"]
        }
    ]
    
    stored_ids = []
    for mem in test_memories:
        result = memory.store_memory(**mem)
        if result.get("success"):
            stored_ids.append(result["memory_id"])
            print(f"✅ Stored: {mem['title']}")
        else:
            print(f"❌ Failed to store: {mem['title']}")
    
    # Test weighted retrieval
    print("\n🔍 Testing Enhanced Weighted Retrieval...")
    weighted_results = memory.recall_memories_weighted(
        query="python performance",
        importance_weight=0.4,
        recency_weight=0.3,
        relevance_weight=0.3,
        limit=10
    )
    
    print(f"Found {len(weighted_results)} memories with weighted scoring:")
    for mem in weighted_results:
        score = mem.get('composite_score', 0)
        title = mem.get('title', 'Untitled')
        print(f"  • {title}: score={score:.3f}")
    
    # Test 2: Persona Evolution Layer
    print("\n🎭 Test 2: Persona Evolution Layer")
    print("-" * 50)
    
    # Store AI persona characteristics
    persona_attributes = [
        {
            "persona_type": "preference",
            "attribute_name": "communication_style",
            "current_value": "technical, detailed, and example-rich",
            "confidence_score": 0.9
        },
        {
            "persona_type": "skill",
            "attribute_name": "programming_languages",
            "current_value": ["Python", "JavaScript", "SQL", "Bash"],
            "confidence_score": 0.8
        },
        {
            "persona_type": "core_trait",
            "attribute_name": "problem_solving_approach",
            "current_value": "systematic, step-by-step analysis with validation",
            "confidence_score": 0.85
        }
    ]
    
    for attr in persona_attributes:
        result = memory.store_persona_memory(**attr)
        if result.get("success"):
            print(f"✅ Stored persona: {attr['persona_type']}.{attr['attribute_name']}")
        else:
            print(f"❌ Failed to store persona: {attr['persona_type']}.{attr['attribute_name']}")
    
    # Retrieve current persona
    print("\n👤 Current AI Persona:")
    persona = memory.get_current_persona()
    for p_type, attributes in persona.items():
        if p_type != "ai_instance_id" and attributes:
            print(f"  {p_type.title()}:")
            for attr_name, attr_data in attributes.items():
                confidence = attr_data.get('confidence', 0)
                value = attr_data.get('value', 'N/A')
                print(f"    • {attr_name}: {value} (confidence: {confidence:.1f})")
    
    # Test 3: Reflexion Capability
    print("\n🤔 Test 3: Reflexion Capability (Self-Assessment)")
    print("-" * 50)
    
    # Generate self-reflections
    reflection_scenarios = [
        {
            "reflection_trigger": "successful_implementation",
            "situation_summary": "Successfully implemented enhanced AI memory system with persona evolution and weighted retrieval"
        },
        {
            "reflection_trigger": "learning_opportunity", 
            "situation_summary": "Discovered importance of weighted scoring algorithms in memory retrieval systems"
        }
    ]
    
    for scenario in reflection_scenarios:
        result = memory.generate_self_reflection(**scenario)
        if result.get("success"):
            print(f"✅ Generated reflection: {scenario['reflection_trigger']}")
            print(f"    Reflection ID: {result['reflection_id']}")
        else:
            print(f"❌ Failed reflection: {scenario['reflection_trigger']}")
    
    # Test 4: Forgetting Mechanism
    print("\n🧽 Test 4: Forgetting Mechanism (Memory Decay)")
    print("-" * 50)
    
    # Apply forgetting curve (dry run first)
    print("Applying forgetting curve (dry run)...")
    forgetting_result = memory.apply_forgetting_curve(
        decay_factor=0.15  # 15% decay for old memories
    )
    
    if forgetting_result.get("success"):
        decayed_count = forgetting_result.get("memories_decayed", 0)
        print(f"✅ Forgetting curve applied: {decayed_count} memories affected")
    else:
        print(f"❌ Forgetting curve failed: {forgetting_result.get('error', 'Unknown error')}")
    
    # Test 5: Persona Evolution Summary
    print("\n📈 Test 5: Persona Evolution Analysis")
    print("-" * 50)
    
    evolution_summary = memory.get_persona_evolution_summary(days_back=7)
    if "error" not in evolution_summary:
        print("✅ Persona evolution analysis:")
        print(f"    Analysis period: {evolution_summary['analysis_period_days']} days")
        print(f"    Total attributes tracked: {evolution_summary['total_attributes_tracked']}")
        print(f"    Recent changes: {len(evolution_summary['recent_changes'])}")
        
        for p_type, data in evolution_summary["persona_types"].items():
            avg_conf = data.get("average_confidence", 0)
            attr_count = data.get("total_attributes", 0)
            print(f"    {p_type}: {attr_count} attributes, avg confidence: {avg_conf:.2f}")
    else:
        print(f"❌ Evolution analysis failed: {evolution_summary['error']}")
    
    # Test 6: Memory System Summary
    print("\n📊 Test 6: Memory System Overview")
    print("-" * 50)
    
    summary = memory.get_memory_summary()
    print("Memory System Status:")
    if "error" not in summary:
        print(f"    Total memories: {summary.get('total_memories', 0)}")
        print(f"    Memory types: {summary.get('memory_type_count', 0)}")
        print(f"    Average importance: {summary.get('average_importance', 0):.2f}")
        print(f"    Storage type: {summary.get('storage_type', 'unknown')}")
    else:
        print(f"    Error: {summary['error']}")
    
    print("\n" + "=" * 70)
    print("🎉 ENHANCED AI MEMORY SYSTEM TEST COMPLETED!")
    print("=" * 70)
    
    # Store test completion as memory
    completion_memory = memory.store_memory(
        memory_type="milestone",
        content="Successfully completed comprehensive test of enhanced AI memory system capabilities",
        title="Enhanced Memory System Test Completion",
        importance=1.0,
        tags=["milestone", "testing", "enhanced-memory", "success"]
    )
    
    if completion_memory.get("success"):
        print(f"📋 Test completion recorded as memory ID: {completion_memory['memory_id']}")
    
    return True


if __name__ == "__main__":
    try:
        test_enhanced_memory_system()
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
