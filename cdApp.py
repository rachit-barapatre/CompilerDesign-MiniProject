import streamlit as st
import re
import json
import time

# --- 1. LEXICAL ANALYZER (LEXER) ---
def lexical_analyzer(query):
    token_specification = [
        ('KEYWORD',    r'\b(SELECT|FROM|WHERE|ORDER\s+BY|BY|ASC|DESC|AND|OR)\b'), 
        ('OPERATOR',   r'[>=<!]+='),                  # >=, <=, !=
        ('SINGLE_OP',  r'[><=]'),                     # >, <, =
        ('NUMBER',     r'\b\d+\b'),                   # Integers
        ('STRING',     r"'(.*?)'|\"(.*?)\""),         # String literals
        ('IDENTIFIER', r'\b[a-zA-Z_][a-zA-Z0-9_]*\b'), # Columns / Tables
        ('COMMA',      r','),                         
        ('SEMICOLON',  r';'),                         
        ('SKIP',       r'[ \t\n\r]+'),                # Spaces & Newlines
        ('MISMATCH',   r'.'),                         # Any other character (Error)
    ]
    
    tok_regex = '|'.join(f'(?P<{name}>{pattern})' for name, pattern in token_specification)
    tokens = []
    
    for mo in re.finditer(tok_regex, query, re.IGNORECASE):
        kind = mo.lastgroup
        value = mo.group()
        
        if kind == 'SKIP':
            continue
        elif kind == 'MISMATCH':
            return None, f"Lexical Error: Unexpected character '{value}'"
            
        if kind == 'KEYWORD':
            # Standardize multi-word keywords like 'ORDER BY'
            value = re.sub(r'\s+', ' ', value.upper())
        elif kind == 'SINGLE_OP':
            kind = 'OPERATOR'
            
        tokens.append({'type': kind, 'value': value})
        
    return tokens, None


# --- 2. SYNTAX ANALYZER & AST GENERATOR (PARSER) ---
class SQLParser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
        
    def peek(self):
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return None
        
    def consume(self, expected_type=None, expected_value=None):
        token = self.peek()
        if not token:
            raise SyntaxError("Unexpected end of query")
            
        if expected_type and token['type'] != expected_type:
            raise SyntaxError(f"Expected {expected_type}, got '{token['value']}'")
        if expected_value and token['value'] != expected_value:
            raise SyntaxError(f"Expected keyword '{expected_value}', got '{token['value']}'")
            
        self.pos += 1
        return token

    def parse(self):
        ast = {}
        
        # Rule 1: SELECT
        self.consume('KEYWORD', 'SELECT')
        ast['action'] = 'SELECT'
        
        # Rule 2: Columns
        columns = []
        columns.append(self.consume('IDENTIFIER')['value'])
        while self.peek() and self.peek()['type'] == 'COMMA':
            self.consume('COMMA')
            columns.append(self.consume('IDENTIFIER')['value'])
        ast['fields'] = columns
        
        # Rule 3: FROM
        self.consume('KEYWORD', 'FROM')
        ast['table'] = self.consume('IDENTIFIER')['value']
        
        # Rule 4: Optional WHERE Clause
        if self.peek() and self.peek()['type'] == 'KEYWORD' and self.peek()['value'] == 'WHERE':
            self.consume('KEYWORD', 'WHERE')
            field = self.consume('IDENTIFIER')['value']
            op = self.consume('OPERATOR')['value']
            
            next_tok = self.peek()
            if next_tok and next_tok['type'] in ['NUMBER', 'STRING']:
                val = self.consume()['value']
            else:
                raise SyntaxError("Expected Number or String in WHERE condition")
            ast['condition'] = {'field': field, 'operator': op, 'value': val}
            
        # Rule 5: Optional ORDER BY Clause (New Feature!)
        if self.peek() and self.peek()['type'] == 'KEYWORD' and self.peek()['value'] == 'ORDER BY':
            self.consume('KEYWORD', 'ORDER BY')
            order_field = self.consume('IDENTIFIER')['value']
            
            # Default sorting order is ASC
            sort_order = 'ASC'
            if self.peek() and self.peek()['type'] == 'KEYWORD' and self.peek()['value'] in ['ASC', 'DESC']:
                sort_order = self.consume()['value']
                
            ast['order_by'] = {'field': order_field, 'direction': sort_order}
            
        # Rule 6: Semicolon
        self.consume('SEMICOLON')
        
        if self.pos < len(self.tokens):
            raise SyntaxError(f"Unexpected tokens after semicolon: '{self.tokens[self.pos]['value']}'")
            
        return ast


# --- 3. SEMANTIC ANALYZER (NEW PHASE) ---
def semantic_analyzer(ast):
    # Check 1: Duplicate column protection
    if len(ast['fields']) != len(set(ast['fields'])):
        return "Semantic Error: Duplicate column names detected in SELECT clause!"
        
    # Check 2: Schema Simulation (Validation check)
    # Target condition fields must not match the table name itself
    if 'condition' in ast and ast['condition']['field'].lower() == ast['table'].lower():
        return f"Semantic Error: Column '{ast['condition']['field']}' cannot have the same name as the target table '{ast['table']}'!"
        
    return None


# --- 4. STREAMLIT USER INTERFACE ---
st.set_page_config(page_title="Advanced SQL Compiler", layout="wide")

st.markdown("<h1 style='text-align: center; color: #4A90E2;'>🚀 Advanced SQL-Like Query Language Compiler Frontend</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>An Academic Prototype featuring <b>Lexical, Syntactic, and Semantic Analysis</b> with AST Generation.</p>", unsafe_allow_html=True)
st.write("---")

# Layout Configuration
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📝 Write SQL Test Statement")
    # New default query including ORDER BY
    default_query = "SELECT name, age, city FROM students WHERE age >= 21 ORDER BY age DESC;"
    query_input = st.text_area("SQL Terminal Input:", value=default_query, height=130)
    compile_btn = st.button("🔥 Run Complete Frontend Compilation", use_container_width=True)

with col2:
    st.subheader("📊 Compiler Metrics & Logs")
    
    if compile_btn:
        start_time = time.time()
        
        # 1. Run Lexer
        tokens, lex_error = lexical_analyzer(query_input)
        
        if lex_error:
            st.error(lex_error)
        else:
            # 2. Run Parser
            parser = SQLParser(tokens)
            try:
                ast_output = parser.parse()
                
                # 3. Run Semantic Analyzer
                semantic_error = semantic_analyzer(ast_output)
                
                if semantic_error:
                    st.error(f"❌ {semantic_error}")
                    if 'tokens' in st.session_state: del st.session_state['tokens']
                    if 'ast' in st.session_state: del st.session_state['ast']
                else:
                    end_time = time.time()
                    duration = (end_time - start_time) * 1000
                    
                    # Metrics Grid
                    m_col1, m_col2, m_col3 = st.columns(3)
                    m_col1.metric("Status", "SUCCESS ✅")
                    m_col2.metric("Tokens Found", f"{len(tokens)}")
                    m_col3.metric("Compilation Time", f"{duration:.2f} ms")
                    
                    st.success("🎉 Lexical, Syntax, and Semantic phases passed seamlessly!")
                    st.session_state['tokens'] = tokens
                    st.session_state['ast'] = ast_output
                    
            except SyntaxError as e:
                st.error(f"❌ Syntax Error: {str(e)}")
                if 'tokens' in st.session_state: del st.session_state['tokens']
                if 'ast' in st.session_state: del st.session_state['ast']
    else:
        st.info("Click the compile button to activate Lexer, Parser, and Semantic checks.")

st.write("---")

# Outputs tabs for clean presentation
if 'tokens' in st.session_state and 'ast' in st.session_state:
    tab1, tab2 = st.tabs(["🔍 Phase 1: Token Stream (Lexer)", "🌳 Phase 2 & 3: Syntax Tree & Semantic Output"])
    
    with tab1:
        st.dataframe(st.session_state['tokens'], use_container_width=True)
        
    with tab2:
        st.json(st.session_state['ast'])
