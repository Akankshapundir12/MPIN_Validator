import re
from datetime import datetime
from typing import List, Tuple, Union, Dict

class MPINValidator:
    def __init__(self):
        self.keypad = [
            ['1', '2', '3'],
            ['4', '5', '6'],
            ['7', '8', '9'],
            ['*', '0', '#']
        ]
        self.keypad_positions = {}
        for i in range(len(self.keypad)):
            for j in range(len(self.keypad[i])):
                self.keypad_positions[self.keypad[i][j]] = (i, j)

    def get_keypad_neighbors(self, digit: str) -> List[str]:
        """Get all possible neighboring digits on the keypad."""
        if digit not in self.keypad_positions:
            return []
        
        i, j = self.keypad_positions[digit]
        neighbors = []
        
        directions = [
            (-1, -1), (-1, 0), (-1, 1),  
            (0, -1),           (0, 1),    
            (1, -1),  (1, 0),  (1, 1)     
        ]
        
        for di, dj in directions:
            ni, nj = i + di, j + dj
            if 0 <= ni < len(self.keypad) and 0 <= nj < len(self.keypad[0]):
                neighbor = self.keypad[ni][nj]
                if neighbor.isdigit():  
                    neighbors.append(neighbor)
        
        return neighbors

    def is_keypad_pattern(self, mpin: str) -> Tuple[bool, List[Tuple[str, str]]]:
        """Check if MPIN follows keypad patterns."""
        reasons = []
        
        horizontal_patterns = ['123', '456', '789']
        vertical_patterns = ['147', '258', '369']
        diagonal_patterns = ['159', '357']
        corner_digits = {'1', '3', '7', '9'}  
        
        for pattern in horizontal_patterns:
            if pattern in mpin or pattern[::-1] in mpin:
                reasons.append(("KEYPAD_HORIZONTAL", f"Horizontal keypad pattern ({pattern})"))
            if pattern * 2 in mpin or (pattern[::-1] * 2) in mpin:
                reasons.append(("KEYPAD_HORIZONTAL", f"Repeated horizontal keypad pattern ({pattern})"))
        
        for pattern in vertical_patterns:
            if pattern in mpin or pattern[::-1] in mpin:
                reasons.append(("KEYPAD_VERTICAL", f"Vertical keypad pattern ({pattern})"))
            if pattern * 2 in mpin or (pattern[::-1] * 2) in mpin:
                reasons.append(("KEYPAD_VERTICAL", f"Repeated vertical keypad pattern ({pattern})"))
        
        for pattern in diagonal_patterns:
            if pattern in mpin or pattern[::-1] in mpin:
                reasons.append(("KEYPAD_DIAGONAL", f"Diagonal keypad pattern ({pattern})"))
            if pattern * 2 in mpin or (pattern[::-1] * 2) in mpin:
                reasons.append(("KEYPAD_DIAGONAL", f"Repeated diagonal keypad pattern ({pattern})"))
        
        mpin_digits = set(mpin)
        if mpin_digits.issubset(corner_digits):
            used_corners = sorted(list(mpin_digits))
            if len(used_corners) == 4:
                reasons.append(("KEYPAD_CORNER", "Common keypad pattern using all four corners"))
            elif len(used_corners) == 3:
                reasons.append(("KEYPAD_CORNER", f"Common keypad pattern using three corners: {', '.join(used_corners)}"))
            elif len(used_corners) == 2:
                reasons.append(("KEYPAD_CORNER", f"Common keypad pattern using two corners: {', '.join(used_corners)}"))
        
        return bool(reasons), reasons

    def is_arithmetic_progression(self, mpin: str) -> Tuple[bool, str]:
        """Check if MPIN forms an arithmetic progression."""
        digits = [int(d) for d in mpin]
        if len(digits) < 2:
            return False, ""
        diff = digits[1] - digits[0]
        is_progression = all(digits[i] - digits[i-1] == diff for i in range(1, len(digits)))
        if is_progression:
            return True, f"Arithmetic progression with difference {diff}"
        return False, ""

    def is_geometric_progression(self, mpin: str) -> Tuple[bool, str]:
        """Check if MPIN forms a geometric progression."""
        digits = [int(d) for d in mpin]
        if len(digits) < 2 or 0 in digits:
            return False, ""
        ratio = digits[1] / digits[0]
        is_progression = all(digits[i] / digits[i-1] == ratio for i in range(1, len(digits)))
        if is_progression:
            return True, f"Geometric progression with ratio {ratio}"
        return False, ""

    def is_repetitive(self, mpin: str) -> Tuple[bool, str]:
        """Check if MPIN has repetitive patterns."""
        if len(set(mpin)) == 1:
            return True, f"All digits are same ({mpin[0]})"
        return False, ""

    def is_ascending(self, mpin: str) -> Tuple[bool, str]:
        """Check if MPIN is in ascending order."""
        is_asc = all(int(mpin[i]) <= int(mpin[i+1]) for i in range(len(mpin)-1))
        if is_asc:
            return True, "Digits are in ascending order"
        return False, ""

    def is_descending(self, mpin: str) -> Tuple[bool, str]:
        """Check if MPIN is in descending order."""
        is_desc = all(int(mpin[i]) >= int(mpin[i+1]) for i in range(len(mpin)-1))
        if is_desc:
            return True, "Digits are in descending order"
        return False, ""

    def is_common_pattern(self, mpin: str) -> Tuple[bool, List[Tuple[str, str]]]:
        """Check if MPIN follows common patterns."""
        reasons = []
        
        if len(mpin) >= 4:
            pairs = [mpin[i:i+2] for i in range(0, len(mpin)-1, 2)]
            if len(set(pairs)) == 1:
                reasons.append(("REPEATED_PAIR", f"Repeated pair pattern ({pairs[0]})"))

        if len(mpin) >= 4:
            for i in range(1, len(mpin)//2 + 1):
                if mpin[:i] * (len(mpin)//i) == mpin:
                    reasons.append(("REPEATED_SEQUENCE", f"Repeated sequence ({mpin[:i]})"))

        is_keypad, keypad_reasons = self.is_keypad_pattern(mpin)
        if is_keypad:
            reasons.extend(keypad_reasons)

        return bool(reasons), reasons

    def extract_date_patterns(self, date_str: str) -> List[str]:
        """Extract possible date patterns from a date string."""
        try:
            date = datetime.strptime(date_str, '%d-%m-%Y')
            patterns = []
            
            patterns.extend([
                date.strftime('%d%m'),  
                date.strftime('%m%d'),  
                date.strftime('%y%m'),  
                date.strftime('%m%y'),  
                date.strftime('%y%d'),  
                date.strftime('%d%y'),  
            ])
            
            patterns.extend([
                date.strftime('%d%m%y'),  
                date.strftime('%y%m%d'),  
                date.strftime('%m%d%y'),  
                date.strftime('%y%d%m'), 
            ])
            
            return patterns
        except ValueError:
            return []

    def extract_year_patterns(self, date_str: str) -> List[str]:
        """Extract year patterns from a date string."""
        try:
            date = datetime.strptime(date_str, '%d-%m-%Y')
            patterns = []
            
            patterns.append(date.strftime('%Y'))
            
            patterns.append(date.strftime('%y'))
            
            return patterns
        except ValueError:
            return []

    def is_subsequence(self, pattern: str, mpin: str) -> bool:
        """Check if pattern is a subsequence of mpin."""
        if len(pattern) <= 1:
            return False
            
        pattern_idx = 0
        for digit in mpin:
            if pattern_idx < len(pattern) and digit == pattern[pattern_idx]:
                pattern_idx += 1
        return pattern_idx == len(pattern)

    def extract_combined_date_patterns(self, dob1: str, dob2: str = None) -> List[str]:
        """Extract combined patterns from two dates."""
        try:
            date1 = datetime.strptime(dob1, '%d-%m-%Y')
            patterns = []
            
            if dob2:
                date2 = datetime.strptime(dob2, '%d-%m-%Y')
                
                d1 = date1.strftime('%d')  
                m1 = date1.strftime('%m')  
                y1 = date1.strftime('%y')  
                                
                d2 = date2.strftime('%d')  
                m2 = date2.strftime('%m')  
                y2 = date2.strftime('%y')  
                
                patterns.append(f"{d1}{d2}")  
                patterns.append(f"{d2}{d1}")  
                
                patterns.append(f"{m1}{m2}")  
                patterns.append(f"{m2}{m1}")  
                
                patterns.append(f"{d1}{m2}")  
                patterns.append(f"{m2}{d1}")  
                
                patterns.append(f"{m1}{d2}")  
                patterns.append(f"{d2}{m1}")  
                
                patterns.append(f"{y1}{y2}")  
                patterns.append(f"{y2}{y1}")  
                
                patterns.append(f"{d1}{y2}")  
                patterns.append(f"{y2}{d1}")  
                
                patterns.append(f"{m1}{y2}")  
                patterns.append(f"{y2}{m1}")  
                
                patterns.append(f"{d2}{y1}")  
                patterns.append(f"{y1}{d2}")  
                
                patterns.append(f"{m2}{y1}")  
                patterns.append(f"{y1}{m2}")  
            
            return patterns
        except ValueError:
            return []

    def validate_mpin(self, mpin: str, dob: str = None, spouse_dob: str = None, 
                     anniversary: str = None) -> Tuple[str, Dict[str, List[str]], int, str]:
        
        if not mpin.isdigit() or len(mpin) not in [4, 6]:
            return 'WEAK', {'INVALID_FORMAT': ['MPIN must be 4 or 6 digits']}, 0, 'red'

        reasons = {}
        pattern_reasons = []
        
        is_common, common_reasons = self.is_common_pattern(mpin)
        if is_common:
            pattern_reasons.extend([reason[1] for reason in common_reasons])

        is_arithmetic, arithmetic_reason = self.is_arithmetic_progression(mpin)
        if is_arithmetic:
            pattern_reasons.append(arithmetic_reason)

        is_geometric, geometric_reason = self.is_geometric_progression(mpin)
        if is_geometric:
            pattern_reasons.append(geometric_reason)

        is_rep, rep_reason = self.is_repetitive(mpin)
        if is_rep:
            pattern_reasons.append(rep_reason)

        is_asc, asc_reason = self.is_ascending(mpin)
        if is_asc:
            pattern_reasons.append(asc_reason)

        is_desc, desc_reason = self.is_descending(mpin)
        if is_desc:
            pattern_reasons.append(desc_reason)

        if pattern_reasons:
            reasons['COMMON_PATTERN'] = pattern_reasons

        dates = []
        if dob:
            dates.append(('self', dob))
        if spouse_dob:
            dates.append(('spouse', spouse_dob))
        if anniversary:
            dates.append(('anniversary', anniversary))

        for i in range(len(dates)):
            for j in range(i + 1, len(dates)):
                date1_type, date1 = dates[i]
                date2_type, date2 = dates[j]
                
                combined_patterns = self.extract_combined_date_patterns(date1, date2)
                for pattern in combined_patterns:
                    if len(pattern) == len(mpin) and pattern == mpin:
                        date1_obj = datetime.strptime(date1, '%d-%m-%Y')
                        date2_obj = datetime.strptime(date2, '%d-%m-%Y')
                        d1 = date1_obj.strftime('%d')
                        m1 = date1_obj.strftime('%m')
                        d2 = date2_obj.strftime('%d')
                        m2 = date2_obj.strftime('%m')
                        
                        if pattern == f"{d1}{d2}":
                            reasons['DEMOGRAPHIC_COMBINED'] = [f"DEMOGRAPHIC_COMBINED : Match with combined pattern (day from {date1_type} DOB {d1} + day from {date2_type} DOB {d2})"]
                        elif pattern == f"{d2}{d1}":
                            reasons['DEMOGRAPHIC_COMBINED'] = [f"DEMOGRAPHIC_COMBINED : Match with combined pattern (day from {date2_type} DOB {d2} + day from {date1_type} DOB {d1})"]
                        elif pattern == f"{d1}{m2}":
                            reasons['DEMOGRAPHIC_COMBINED'] = [f"DEMOGRAPHIC_COMBINED : Match with combined pattern (day from {date1_type} DOB {d1} + month from {date2_type} DOB {m2})"]
                        elif pattern == f"{m2}{d1}":
                            reasons['DEMOGRAPHIC_COMBINED'] = [f"DEMOGRAPHIC_COMBINED : Match with combined pattern (month from {date2_type} DOB {m2} + day from {date1_type} DOB {d1})"]
                        elif pattern == f"{m1}{d2}":
                            reasons['DEMOGRAPHIC_COMBINED'] = [f"DEMOGRAPHIC_COMBINED : Match with combined pattern (month from {date1_type} DOB {m1} + day from {date2_type} DOB {d2})"]
                        elif pattern == f"{d2}{m1}":
                            reasons['DEMOGRAPHIC_COMBINED'] = [f"DEMOGRAPHIC_COMBINED : Match with combined pattern (day from {date2_type} DOB {d2} + month from {date1_type} DOB {m1})"]
                        else:
                            reasons['DEMOGRAPHIC_COMBINED'] = [f"DEMOGRAPHIC_COMBINED : Match with combined pattern from {date1_type} and {date2_type} DOBs"]
                        break
                    elif self.is_subsequence(pattern, mpin):
                        reasons['DEMOGRAPHIC_COMBINED'] = [f"DEMOGRAPHIC_COMBINED : Contains subsequence from combined {date1_type} and {date2_type} DOB pattern"]
                        break

        if dob:
            year_patterns = self.extract_year_patterns(dob)
            for pattern in year_patterns:
                if len(pattern) == len(mpin) and pattern == mpin:
                    reasons['DEMOGRAPHIC_DOB_SELF'] = [f"DEMOGRAPHIC_DOB_SELF : Match with your birth year ({dob})"]
                    break
                elif self.is_subsequence(pattern, mpin):
                    reasons['DEMOGRAPHIC_DOB_SELF'] = [f"DEMOGRAPHIC_DOB_SELF : Contains subsequence from your birth year ({dob})"]
                    break
            
            dob_patterns = self.extract_date_patterns(dob)
            for pattern in dob_patterns:
                if len(pattern) == len(mpin) and pattern == mpin:
                    reasons['DEMOGRAPHIC_DOB_SELF'] = [f"DEMOGRAPHIC_DOB_SELF : Match with your date of birth ({dob})"]
                    break
                elif self.is_subsequence(pattern, mpin):
                    reasons['DEMOGRAPHIC_DOB_SELF'] = [f"DEMOGRAPHIC_DOB_SELF : Contains subsequence from your date of birth ({dob})"]
                    break
        
        if spouse_dob:
            year_patterns = self.extract_year_patterns(spouse_dob)
            for pattern in year_patterns:
                if len(pattern) == len(mpin) and pattern == mpin:
                    reasons['DEMOGRAPHIC_DOB_SPOUSE'] = [f"DEMOGRAPHIC_DOB_SPOUSE : Match with spouse's birth year ({spouse_dob})"]
                    break
                elif self.is_subsequence(pattern, mpin):
                    reasons['DEMOGRAPHIC_DOB_SPOUSE'] = [f"DEMOGRAPHIC_DOB_SPOUSE : Contains subsequence from spouse's birth year ({spouse_dob})"]
                    break
            
            spouse_dob_patterns = self.extract_date_patterns(spouse_dob)
            for pattern in spouse_dob_patterns:
                if len(pattern) == len(mpin) and pattern == mpin:
                    reasons['DEMOGRAPHIC_DOB_SPOUSE'] = [f"DEMOGRAPHIC_DOB_SPOUSE : Match with spouse's date of birth ({spouse_dob})"]
                    break
                elif self.is_subsequence(pattern, mpin):
                    reasons['DEMOGRAPHIC_DOB_SPOUSE'] = [f"DEMOGRAPHIC_DOB_SPOUSE : Contains subsequence from spouse's date of birth ({spouse_dob})"]
                    break
        
        if anniversary:
            year_patterns = self.extract_year_patterns(anniversary)
            for pattern in year_patterns:
                if len(pattern) == len(mpin) and pattern == mpin:
                    reasons['DEMOGRAPHIC_ANNIVERSARY'] = [f"DEMOGRAPHIC_ANNIVERSARY : Match with wedding anniversary year ({anniversary})"]
                    break
            
            anniversary_patterns = self.extract_date_patterns(anniversary)
            for pattern in anniversary_patterns:
                if len(pattern) == len(mpin) and pattern == mpin:
                    reasons['DEMOGRAPHIC_ANNIVERSARY'] = [f"DEMOGRAPHIC_ANNIVERSARY : Match with wedding anniversary date ({anniversary})"]
                    break
                elif self.is_subsequence(pattern, mpin):
                    reasons['DEMOGRAPHIC_ANNIVERSARY'] = [f"DEMOGRAPHIC_ANNIVERSARY : Contains subsequence from wedding anniversary date ({anniversary})"]
                    break

        strength_percentage = self.calculate_strength_percentage(reasons)
        
        if strength_percentage >= 70:
            strength = 'STRONG'
            color = 'green'
        else:
            strength = 'WEAK'
            color = 'red'
        
        return strength, reasons, strength_percentage, color

    def calculate_strength_percentage(self, reasons: Dict[str, List[str]]) -> int:
        """Calculate strength percentage based on reasons."""
        if not reasons:
            return 100
        
        base_strength = 100
        deductions = {
            'REPETITIVE': 35,      
            'ASCENDING': 35,       
            'DESCENDING': 35,      
            'ARITHMETIC': 40,      
            'GEOMETRIC': 10,       
            'KEYPAD_HORIZONTAL': 35,  
            'KEYPAD_VERTICAL': 35,    
            'KEYPAD_DIAGONAL': 35,    
            'KEYPAD_CORNER': 35,      
            'REPEATED_PAIR': 35,      
            'REPEATED_SEQUENCE': 35,  
            'DEMOGRAPHIC_DOB_SELF': 40,    
            'DEMOGRAPHIC_DOB_SPOUSE': 40,  
            'DEMOGRAPHIC_ANNIVERSARY': 40, 
            'DEMOGRAPHIC_COMBINED': 20,    
        }
        
        total_deduction = 0
        for reason, explanations in reasons.items():
            if reason == 'COMMON_PATTERN':
                for explanation in explanations:
                    if 'Arithmetic progression' in explanation:
                        total_deduction += deductions['ARITHMETIC']
                    elif 'Geometric progression' in explanation:
                        total_deduction += deductions['GEOMETRIC']
                    elif 'All digits are same' in explanation:
                        total_deduction += deductions['REPETITIVE']
                    elif 'Digits are in ascending order' in explanation:
                        total_deduction += deductions['ASCENDING']
                    elif 'Digits are in descending order' in explanation:
                        total_deduction += deductions['DESCENDING']
                    elif 'Repeated pair pattern' in explanation:
                        total_deduction += deductions['REPEATED_PAIR']
                    elif 'Repeated sequence' in explanation:
                        total_deduction += deductions['REPEATED_SEQUENCE']
                    elif 'Horizontal keypad pattern' in explanation:
                        total_deduction += deductions['KEYPAD_HORIZONTAL']
                    elif 'Vertical keypad pattern' in explanation:
                        total_deduction += deductions['KEYPAD_VERTICAL']
                    elif 'Diagonal keypad pattern' in explanation:
                        total_deduction += deductions['KEYPAD_DIAGONAL']
                    elif 'Common keypad pattern using' in explanation:
                        total_deduction += deductions['KEYPAD_CORNER']
            elif reason.startswith('DEMOGRAPHIC_'):
                for explanation in explanations:
                    if 'Match with' in explanation:
                        if 'birth year' in explanation or 'anniversary year' in explanation:
                            total_deduction += 20  
                        elif reason == 'DEMOGRAPHIC_COMBINED':
                            total_deduction += deductions['DEMOGRAPHIC_COMBINED']  
                        else:
                            total_deduction += deductions[reason]
                    elif 'Contains subsequence' in explanation:
                        if 'birth year' in explanation or 'anniversary year' in explanation:
                            total_deduction += 5  
                        elif reason == 'DEMOGRAPHIC_COMBINED':
                            total_deduction += 5  
                        else:
                            total_deduction += 10 
            else:
                total_deduction += deductions.get(reason, 0)
        
        return max(0, base_strength - total_deduction)