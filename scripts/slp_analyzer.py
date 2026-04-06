#!/usr/bin/env python3
"""
SLP (Speech-Language Pathology) analysis module.
Analyzes prosody, intelligibility, fatigue markers, and TBI patterns.
"""

import json
import re
from datetime import datetime

class SLPAnalyzer:
    """Analyzes speech pathology markers from transcripts."""
    
    def __init__(self):
        self.markers = {
            'prosody': {},
            'intelligibility': {},
            'fatigue_markers': {},
            'tbi_patterns': {},
            'cognitive_markers': {}
        }
    
    def analyze(self, transcript, speakers=None):
        """Run complete SLP analysis on transcript."""
        analysis = {
            'timestamp': datetime.now().isoformat(),
            'transcript_length': len(transcript),
            'word_count': len(transcript.split()),
        }
        
        # Analyze markers
        analysis['prosody'] = self._analyze_prosody(transcript)
        analysis['intelligibility'] = self._analyze_intelligibility(transcript)
        analysis['fatigue_markers'] = self._analyze_fatigue(transcript)
        analysis['tbi_patterns'] = self._analyze_tbi_markers(transcript)
        analysis['cognitive_markers'] = self._analyze_cognitive(transcript)
        
        # Speaker patterns if available
        if speakers:
            analysis['speaker_patterns'] = self._analyze_speakers(transcript, speakers)
        
        # Overall assessment
        analysis['overall_assessment'] = self._generate_assessment(analysis)
        
        return analysis
    
    def _analyze_prosody(self, transcript):
        """Analyze rate, rhythm, intonation indicators."""
        return {
            'filled_pauses': len(re.findall(r'\bum\b|\buh\b|\bah\b', transcript, re.I)),
            'word_repetitions': len(re.findall(r'\b(\w+)\s+\1\b', transcript, re.I)),
            'stuttering_indicators': len(re.findall(r'\b(\w)\1{2,}', transcript)),
            'ellipsis_count': transcript.count('...'),
            'notes': 'Filled pauses and repetitions may indicate cognitive load or fatigue'
        }
    
    def _analyze_intelligibility(self, transcript):
        """Assess speech clarity and articulation."""
        unclear_markers = len(re.findall(r'\[unclear\]|\?{2,}|\[inaudible\]', transcript, re.I))
        return {
            'unclear_segments': unclear_markers,
            'sentence_fragments': transcript.count('...'),
            'clarity_score': 'high' if unclear_markers < 5 else 'medium' if unclear_markers < 10 else 'low',
            'notes': 'Based on transcription clarity and fragment patterns'
        }
    
    def _analyze_fatigue(self, transcript):
        """Identify markers of fatigue, voice changes, effort."""
        return {
            'long_utterances': len(re.findall(r'[^.!?]*[.!?]', transcript)) // max(1, len(transcript) // 100),
            'pause_frequency': transcript.count('...') + transcript.count('–'),
            'effort_language': len(re.findall(r'\b(exhausted|tired|hard|difficult|struggling)\b', transcript, re.I)),
            'voice_change_mentions': len(re.findall(r'\b(hoarse|quiet|whisper|struggling)\b', transcript, re.I)),
            'notes': 'Fatigue may manifest as shorter phrases, more pauses, explicit effort mentions'
        }
    
    def _analyze_tbi_markers(self, transcript):
        """Identify patterns consistent with TBI effects."""
        return {
            'word_finding_pauses': len(re.findall(r'\.{2,}|\b(um|uh|what\'s that word)\b', transcript, re.I)),
            'topic_maintenance': self._assess_topic_coherence(transcript),
            'memory_references': len(re.findall(r'\b(don\'t remember|forgot|can\'t recall)\b', transcript, re.I)),
            'processing_time': 'indicated by pauses and filled pauses',
            'notes': 'TBI may affect word retrieval, topic organization, memory references'
        }
    
    def _analyze_cognitive(self, transcript):
        """Assess cognitive-linguistic markers."""
        sentences = re.split(r'[.!?]+', transcript)
        valid_sentences = [s.strip() for s in sentences if len(s.strip().split()) > 3]
        
        return {
            'sentence_complexity': 'simple' if len(valid_sentences) > len(sentences) * 0.7 else 'complex',
            'average_utterance_length': len(transcript.split()) / max(1, len(valid_sentences)),
            'vocabulary_diversity': len(set(transcript.lower().split())) / max(1, len(transcript.split())),
            'topic_shifts': len(re.findall(r'\n|But|However|Anyway', transcript)),
            'notes': 'Shorter utterances and simple sentences may indicate cognitive load'
        }
    
    def _assess_topic_coherence(self, transcript):
        """Rate how well speaker maintains topic."""
        # Simple heuristic: if there are many topic shift markers, coherence is lower
        shifts = len(re.findall(r'\banyway\b|\bbut\b|\bso\b|\bby the way\b', transcript, re.I))
        length = len(transcript.split())
        shift_ratio = shifts / max(1, length / 100)
        
        if shift_ratio < 1:
            return 'high'
        elif shift_ratio < 3:
            return 'medium'
        else:
            return 'low'
    
    def _analyze_speakers(self, transcript, speakers):
        """Analyze patterns across speakers if diarization available."""
        return {
            'speaker_count': len(speakers),
            'speaker_names': list(speakers.keys()),
            'turn_taking_pattern': 'mixed participation',
            'notes': 'Speaker diarization identifies different voices in conversation'
        }
    
    def _generate_assessment(self, analysis):
        """Generate summary clinical assessment."""
        fatigue_markers = analysis['fatigue_markers'].get('effort_language', 0)
        tbi_markers = analysis['tbi_patterns'].get('word_finding_pauses', 0)
        clarity = analysis['intelligibility'].get('clarity_score', 'unknown')
        
        assessment = {
            'fatigue_level': 'high' if fatigue_markers > 3 else 'medium' if fatigue_markers > 0 else 'low',
            'cognitive_effort_evident': tbi_markers > 5,
            'speech_clarity': clarity,
            'clinical_notes': 'Transcript shows characteristic patterns. Recommend review by SLP for formal assessment.'
        }
        
        return assessment

