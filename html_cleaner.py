import logging
import os
from datetime import datetime
from urllib.parse import urlparse
from bs4 import BeautifulSoup, Comment
import re
from collections import Counter
from difflib import SequenceMatcher
import hashlib

class HtmlCleaner:
    def __init__(self, temp_dir="temp"):
        self.logger = logging.getLogger(__name__)
        self.temp_dir = temp_dir
        self.cleaned_html_dir = os.path.join(temp_dir, "cleaned_html")
        os.makedirs(self.cleaned_html_dir, exist_ok=True)
        
        self.header_tags = ['header', 'nav', 'aside']
        self.footer_tags = ['footer']
        self.noise_tags = ['script', 'style', 'meta', 'link', 'noscript']
        
        # Non-essential attributes that can be safely removed without affecting data extraction
        self.remove_attributes = [
            # Styling and presentation (but NOT class/id - they're needed for BS4 selectors)
            'style',
            
            # JavaScript event handlers
            'onclick', 'onload', 'onerror', 'onmouseover', 'onmouseout', 'onmousedown', 'onmouseup',
            'onfocus', 'onblur', 'onchange', 'onsubmit', 'onreset', 'onkeydown', 'onkeyup', 'onkeypress',
            'ondblclick', 'oncontextmenu', 'onwheel', 'ondrag', 'ondrop', 'ondragover', 'ondragenter',
            'ondragleave', 'ondragstart', 'ondragend', 'onscroll', 'onresize', 'onselect',
            
            # Analytics and tracking
            'data-analytics', 'data-tracking', 'data-ga', 'data-gtm', 'data-fb', 'data-pixel',
            'data-track', 'data-event', 'data-label', 'data-category', 'data-action',
            'data-google-analytics', 'data-mixpanel', 'data-segment', 'data-amplitude',
            
            # Testing and debugging
            'data-testid', 'data-test', 'data-cy', 'data-selenium', 'data-qa', 'data-automation',
            'data-e2e', 'data-test-id', 'data-jest', 'data-playwright',
            
            # Accessibility (only non-essential ones)
            'aria-describedby', 'aria-labelledby', 'aria-controls', 'aria-owns',
            'aria-flowto', 'aria-activedescendant', 'aria-details',
            
            # Interaction and usability (non-essential)
            'tabindex', 'accesskey', 'draggable', 'spellcheck', 'contenteditable',
            'autocomplete', 'autocapitalize', 'autocorrect',
            
            # Layout and positioning (CSS-related)
            'align', 'valign', 'bgcolor', 'background', 'border', 'cellpadding', 'cellspacing',
            'width', 'height', 'size', 'color', 'face', 'clear',
            
            # Meta information (SEO/social)
            'data-description', 'data-keywords', 'data-author', 'data-copyright',
            'data-og-', 'data-twitter-', 'data-fb-', 'data-linkedin-',
            
            # Framework/library specific (non-essential)
            'data-react', 'data-vue', 'data-angular', 'data-ember', 'data-backbone',
            'ng-', 'v-', 'x-data', 'x-show', 'x-if', 'alpine-',
            
            # Performance and loading
            'loading', 'decoding', 'fetchpriority', 'referrerpolicy',
            
            # Form validation styling
            'data-valid', 'data-invalid', 'data-error', 'data-success',
            
            # Animation and transition
            'data-animate', 'data-animation', 'data-transition', 'data-duration',
            'data-delay', 'data-ease',
            
            # Theme and appearance
            'data-theme', 'data-mode', 'data-variant', 'data-color-scheme',
            
            # Tooltip and popover positioning
            'data-placement', 'data-offset', 'data-boundary', 'data-flip',
            
            # Security (non-essential)
            'crossorigin', 'integrity', 'nonce'
        ]
        
        # Essential attributes that should NEVER be removed (critical for data extraction and BS4 selectors)
        self.essential_attributes = {
            # Core content attributes and selectors
            'id', 'class', 'name', 'value', 'content', 'text', 'innerHTML', 'innerText',
            
            # Links and navigation
            'href', 'src', 'action', 'target', 'download',
            
            # Form data
            'type', 'placeholder', 'required', 'disabled', 'readonly', 'checked', 'selected',
            'multiple', 'accept', 'pattern', 'min', 'max', 'step', 'minlength', 'maxlength',
            
            # Essential meta information
            'title', 'alt', 'lang', 'charset', 'encoding',
            
            # Data attributes that might contain extractable data
            'data-price', 'data-value', 'data-id', 'data-name', 'data-title', 'data-url',
            'data-date', 'data-time', 'data-location', 'data-phone', 'data-email',
            'data-rating', 'data-review', 'data-count', 'data-quantity', 'data-amount',
            'data-currency', 'data-status', 'data-category', 'data-type', 'data-brand',
            'data-model', 'data-sku', 'data-description', 'data-summary',
            
            # Essential accessibility (content-related)
            'aria-label', 'aria-hidden', 'aria-expanded', 'aria-selected', 'aria-checked',
            'aria-pressed', 'aria-current', 'aria-live', 'aria-atomic', 'role',
            
            # Media attributes
            'controls', 'autoplay', 'loop', 'muted', 'poster', 'preload',
            
            # Table structure
            'colspan', 'rowspan', 'headers', 'scope',
            
            # List structure
            'start', 'reversed',
            
            # Essential form attributes
            'for', 'form', 'method', 'enctype', 'novalidate',
            
            # Common selector attributes used in BeautifulSoup
            'rel', 'property', 'itemprop', 'itemtype', 'itemscope',
            
            # Custom data attributes commonly used for content identification
            'data-role', 'data-component', 'data-module', 'data-section',
            'data-element', 'data-widget', 'data-container'
        }
        
    def remove_noise(self, soup):
        """Remove script tags, styles, comments and other noise"""
        # Remove script and style elements
        for tag_name in self.noise_tags:
            for element in soup.find_all(tag_name):
                element.decompose()
        
        # Remove HTML comments
        for comment in soup.find_all(string=lambda text: isinstance(text, Comment)):
            comment.extract()
        
        return soup
    
    def remove_header_footer(self, soup):
        """Remove header and footer elements"""
        # Remove by semantic tags
        for tag_name in self.header_tags + self.footer_tags:
            for element in soup.find_all(tag_name):
                element.decompose()
        
        # Remove by common class/id patterns
        header_patterns = ['header', 'nav', 'navigation', 'menu', 'top-bar', 'masthead']
        footer_patterns = ['footer', 'bottom', 'copyright', 'legal']
        
        for pattern in header_patterns + footer_patterns:
            # Remove by class
            for element in soup.find_all(class_=re.compile(pattern, re.I)):
                element.decompose()
            # Remove by id
            for element in soup.find_all(id=re.compile(pattern, re.I)):
                element.decompose()
        
        return soup
    
    def get_element_signature(self, element):
        """Generate a signature for an element based on its structure"""
        if not element.name:
            return None
            
        # Create signature from tag structure, classes, and attribute patterns
        signature_parts = []
        
        # Tag name
        signature_parts.append(element.name)
        
        # Classes (sorted for consistency)
        if element.get('class'):
            classes = sorted(element.get('class'))
            signature_parts.append('classes:' + ','.join(classes))
        
        # Important attributes (excluding unique identifiers)
        important_attrs = ['role', 'type', 'data-*']
        for attr in element.attrs:
            if attr in important_attrs or attr.startswith('data-'):
                signature_parts.append(f"{attr}:{element.attrs[attr]}")
        
        # Child element structure (first level only)
        child_tags = []
        for child in element.children:
            if hasattr(child, 'name') and child.name:
                child_tags.append(child.name)
        if child_tags:
            signature_parts.append('children:' + ','.join(sorted(set(child_tags))))
        
        return '|'.join(signature_parts)
    
    def find_similar_elements(self, soup, similarity_threshold=0.8, min_occurrences=3):
        """Find elements with similar structure that might be duplicates"""
        body = soup.find('body')
        if not body:
            return []
        
        # Get all elements that could be potential duplicates
        potential_containers = body.find_all(['div', 'article', 'section', 'li', 'tr'])
        
        # Generate signatures for all elements
        signatures = {}
        element_map = {}
        
        for element in potential_containers:
            # Skip if element is too small or too nested
            if len(str(element)) < 100:
                continue
            
            signature = self.get_element_signature(element)
            if not signature:
                continue
                
            if signature not in signatures:
                signatures[signature] = []
                element_map[signature] = []
            
            signatures[signature].append(element)
            element_map[signature].append(element)
        
        # Find signatures that appear multiple times
        duplicate_groups = []
        for signature, elements in signatures.items():
            if len(elements) >= min_occurrences:
                # Additional similarity check using text content structure
                text_signatures = []
                for elem in elements:
                    text = elem.get_text(strip=True)
                    # Create a pattern from text structure (word count, numbers, etc.)
                    words = len(text.split())
                    numbers = len(re.findall(r'\d+', text))
                    text_signatures.append(f"words:{words},numbers:{numbers}")
                
                # Group by similar text signatures
                text_counter = Counter(text_signatures)
                most_common_text_sig = text_counter.most_common(1)[0]
                
                if most_common_text_sig[1] >= min_occurrences:
                    duplicate_groups.append(elements)
        
        return duplicate_groups
    
    def get_structural_hash(self, element):
        """Generate a structural hash for an element based on its DOM structure"""
        def get_element_tree_structure(elem, max_depth=3, current_depth=0):
            """Recursively build a structure representation"""
            if current_depth >= max_depth or not hasattr(elem, 'name') or not elem.name:
                return ""
            
            structure_parts = [elem.name]
            
            # Add important attributes (sorted for consistency)
            if elem.get('class'):
                structure_parts.append(f"class:{','.join(sorted(elem.get('class')))}")
            
            # Add child structure
            child_structures = []
            for child in elem.children:
                if hasattr(child, 'name') and child.name:
                    child_structure = get_element_tree_structure(child, max_depth, current_depth + 1)
                    if child_structure:
                        child_structures.append(child_structure)
            
            if child_structures:
                structure_parts.append(f"children:[{','.join(child_structures)}]")
            
            return '|'.join(structure_parts)
        
        structure_str = get_element_tree_structure(element)
        return hashlib.md5(structure_str.encode()).hexdigest()[:16]
    
    def find_repeating_structures(self, soup, min_keep=2, min_total=3, similarity_threshold=0.85):
        """
        Find repeating HTML structures and keep only a sample of each type.
        
        Args:
            soup: BeautifulSoup object
            min_keep: Minimum number of similar elements to keep (default: 2)
            min_total: Minimum total occurrences to consider as repeating (default: 3)
            similarity_threshold: Structure similarity threshold (0.0-1.0, default: 0.85)
        
        Returns:
            List of elements to remove
        """
        body = soup.find('body')
        if not body:
            return []
        
        # Get potential repeating containers (cards, items, etc.)
        candidates = body.find_all(['div', 'article', 'section', 'li', 'tr'], recursive=True)
        
        # Filter candidates - focus on meaningful containers
        meaningful_candidates = []
        for elem in candidates:
            elem_str = str(elem)
            elem_text = elem.get_text(strip=True)
            
            # Skip if too small, too large, or mostly empty
            if (len(elem_str) < 200 or len(elem_str) > 10000 or 
                len(elem_text) < 10 or len(elem_text) > 2000):
                continue
                
            # Skip if it's mostly nested (likely a wrapper)
            direct_text = elem.get_text(strip=True)
            child_text = ""
            for child in elem.children:
                if hasattr(child, 'get_text'):
                    child_text += child.get_text(strip=True)
            
            if len(direct_text) < len(child_text) * 0.1:  # Less than 10% direct content
                continue
                
            meaningful_candidates.append(elem)
        
        # Group by structural hash
        structure_groups = {}
        for elem in meaningful_candidates:
            struct_hash = self.get_structural_hash(elem)
            if struct_hash not in structure_groups:
                structure_groups[struct_hash] = []
            structure_groups[struct_hash].append(elem)
        
        # Find similar structures using SequenceMatcher for fine-tuning
        similar_groups = {}
        processed_hashes = set()
        
        for hash1, group1 in structure_groups.items():
            if hash1 in processed_hashes or len(group1) < min_total:
                continue
                
            # Start a new similarity group
            similar_group = list(group1)
            group_key = hash1
            processed_hashes.add(hash1)
            
            # Compare with other groups
            for hash2, group2 in structure_groups.items():
                if hash2 in processed_hashes or len(group2) < min_total:
                    continue
                
                # Use SequenceMatcher to compare structure strings
                elem1_str = self.get_element_signature(group1[0]) or ""
                elem2_str = self.get_element_signature(group2[0]) or ""
                
                similarity = SequenceMatcher(None, elem1_str, elem2_str).ratio()
                
                if similarity >= similarity_threshold:
                    similar_group.extend(group2)
                    processed_hashes.add(hash2)
            
            if len(similar_group) >= min_total:
                similar_groups[group_key] = similar_group
        
        # Determine which elements to remove
        elements_to_remove = []
        
        for group_key, elements in similar_groups.items():
            if len(elements) >= min_total:
                # Sort by position in document to keep the first ones
                elements_with_pos = []
                for elem in elements:
                    pos = 0
                    current = elem
                    while current.previous_sibling:
                        pos += 1
                        current = current.previous_sibling
                    elements_with_pos.append((pos, elem))
                
                # Sort by position and keep only the first min_keep elements
                elements_with_pos.sort(key=lambda x: x[0])
                elements_to_keep = [elem for _, elem in elements_with_pos[:min_keep]]
                elements_to_remove_from_group = [elem for _, elem in elements_with_pos[min_keep:]]
                
                elements_to_remove.extend(elements_to_remove_from_group)
                
                self.logger.info(f"Found {len(elements)} similar structures, keeping {len(elements_to_keep)}, removing {len(elements_to_remove_from_group)}")
        
        return elements_to_remove
    
    def remove_repeating_structures(self, soup, min_keep=2, min_total=3, similarity_threshold=0.85):
        """Remove repeating structures while keeping a sample of each type"""
        elements_to_remove = self.find_repeating_structures(soup, min_keep, min_total, similarity_threshold)
        
        removed_count = 0
        for element in elements_to_remove:
            if element.parent:  # Check if still in tree
                element.decompose()
                removed_count += 1
        
        self.logger.info(f"Removed {removed_count} repeating structure elements")
        return soup

    def focus_on_main_content(self, soup):
        """Try to identify and focus on the main content area"""
        main_content_selectors = [
            'main', '[role="main"]', '#main', '.main',
            '#content', '.content', '#main-content', '.main-content',
            'article', '.article', '#article',
            '.container .content', '.page-content'
        ]
        
        for selector in main_content_selectors:
            try:
                main_element = soup.select_one(selector)
                if main_element and len(main_element.get_text(strip=True)) > 500:
                    self.logger.info(f"Found main content using selector: {selector}")
                    # Create new soup with just the main content
                    new_soup = BeautifulSoup(str(main_element), 'html.parser')
                    return new_soup
            except:
                continue
        
        # If no main content found, return body content
        body = soup.find('body')
        if body:
            return BeautifulSoup(str(body), 'html.parser')
        
        return soup
    
    def limit_select_options(self, soup, max_options=2):
        """Limit select tags to keep only a maximum number of option tags"""
        select_tags = soup.find_all('select')
        modified_count = 0
        
        for select_tag in select_tags:
            option_tags = select_tag.find_all('option')
            
            if len(option_tags) > max_options:
                # Keep only the first max_options option tags
                options_to_keep = option_tags[:max_options]
                options_to_remove = option_tags[max_options:]
                
                # Remove excess option tags
                for option in options_to_remove:
                    option.decompose()
                
                modified_count += 1
                self.logger.debug(f"Limited select tag to {max_options} options (removed {len(options_to_remove)} options)")
        
        if modified_count > 0:
            self.logger.info(f"Limited {modified_count} select tags to {max_options} option tags each")
        
        return soup

    def remove_empty_divs_recursive(self, soup):
        """Recursively remove empty div elements starting from innermost"""
        def has_meaningful_content(element):
            """Check if an element has meaningful text content"""
            if not element:
                return False
            
            # Get text content and strip whitespace
            text = element.get_text(strip=True)
            if text:
                return True
            
            # Check for meaningful attributes that indicate the div serves a purpose
            # (like images, inputs, or other interactive elements)
            meaningful_tags = ['img', 'input', 'button', 'a', 'form', 'iframe', 'video', 'audio', 'canvas', 'svg']
            for tag in meaningful_tags:
                if element.find(tag):
                    return True
            
            # Check for data attributes or specific classes that might indicate functionality
            if element.get('data-') or element.get('id'):
                # Be more selective - only keep if it seems functional
                attrs = element.attrs
                for attr_name in attrs:
                    if attr_name.startswith('data-') and not attr_name.startswith('data-testid'):
                        return True
                    if attr_name == 'id' and not any(x in str(attrs[attr_name]).lower() for x in ['placeholder', 'skeleton', 'loading']):
                        return True
            
            return False
        
        def remove_empty_divs_pass(soup):
            """Single pass of empty div removal"""
            removed_count = 0
            
            # Find all div elements, starting from deepest nesting
            all_divs = soup.find_all('div')
            
            # Sort by nesting depth (deepest first) to handle innermost divs first
            divs_by_depth = []
            for div in all_divs:
                depth = len(list(div.parents))
                divs_by_depth.append((depth, div))
            
            # Sort by depth in descending order (deepest first)
            divs_by_depth.sort(key=lambda x: x[0], reverse=True)
            
            for depth, div in divs_by_depth:
                if div.parent is None:  # Already removed
                    continue
                
                if not has_meaningful_content(div):
                    # Check if removing this div would break structure
                    parent = div.parent
                    if parent and parent.name in ['html', 'head', 'body']:
                        # Don't remove direct children of important structural elements
                        # unless they're completely empty
                        if not div.get_text(strip=True) and not div.find_all():
                            div.decompose()
                            removed_count += 1
                    else:
                        div.decompose()
                        removed_count += 1
            
            return removed_count
        
        # Keep removing empty divs until no more can be removed
        total_removed = 0
        max_iterations = 10  # Prevent infinite loops
        iteration = 0
        
        while iteration < max_iterations:
            removed_this_pass = remove_empty_divs_pass(soup)
            total_removed += removed_this_pass
            
            if removed_this_pass == 0:
                break  # No more empty divs to remove
                
            iteration += 1
        
        self.logger.info(f"Removed {total_removed} empty div elements in {iteration} iterations")
        return soup
    
    def remove_whitespace_between_tags(self, html_content):
        """
        Remove whitespace and newlines only between consecutive tags while preserving 
        text content within tags. This compresses the HTML size without affecting 
        the actual content.
        
        Args:
            html_content (str): HTML content as string
            
        Returns:
            str: HTML with whitespace between tags removed
        """
        original_length = len(html_content)
        
        # Use regex to remove whitespace between closing tag and opening tag
        # Pattern explanation:
        # (>\s+<) matches: > followed by one or more whitespace chars followed by <
        # Replace with: ><
        cleaned_html = re.sub(r'>\s+<', '><', html_content)
        
        # Also remove leading/trailing whitespace from lines but preserve content structure
        lines = cleaned_html.split('\n')
        cleaned_lines = []
        
        for line in lines:
            stripped_line = line.strip()
            if stripped_line:  # Only keep non-empty lines
                cleaned_lines.append(stripped_line)
        
        # Join lines without extra newlines
        final_html = ''.join(cleaned_lines)
        
        final_length = len(final_html)
        reduction_percent = ((original_length - final_length) / original_length * 100) if original_length > 0 else 0
        
        self.logger.info(f"Removed whitespace between tags. Length: {original_length} → {final_length} "
                        f"({reduction_percent:.1f}% reduction)")
        
        return final_html
    
    def remove_non_essential_attributes(self, soup):
        """
        Remove non-essential HTML attributes that don't affect data extraction.
        
        This method removes styling, tracking, testing, and other non-content attributes
        while preserving all attributes that might contain extractable data.
        
        Args:
            soup: BeautifulSoup object
            
        Returns:
            BeautifulSoup object with non-essential attributes removed
        """
        removed_count = 0
        total_attributes_before = 0
        
        # Get all elements with attributes
        all_elements = soup.find_all(lambda tag: tag.attrs)
        
        for element in all_elements:
            if not element.attrs:
                continue
                
            original_attrs = dict(element.attrs)
            total_attributes_before += len(original_attrs)
            attributes_to_remove = []
            
            for attr_name in original_attrs:
                # Skip if it's an essential attribute
                if attr_name in self.essential_attributes:
                    continue
                
                # Check for exact matches
                if attr_name in self.remove_attributes:
                    attributes_to_remove.append(attr_name)
                    continue
                
                # Check for pattern matches (like data-* attributes)
                should_remove = False
                for remove_pattern in self.remove_attributes:
                    if remove_pattern.endswith('-') and attr_name.startswith(remove_pattern):
                        # Handle patterns like 'data-og-', 'ng-', etc.
                        should_remove = True
                        break
                
                if should_remove:
                    attributes_to_remove.append(attr_name)
                    continue
                
                # Special handling for data attributes - be more selective
                if attr_name.startswith('data-'):
                    # Check if it's a data attribute that might contain useful content
                    data_key = attr_name[5:]  # Remove 'data-' prefix
                    
                    # Keep data attributes that are likely to contain extractable content
                    useful_data_patterns = [
                        'price', 'value', 'id', 'name', 'title', 'url', 'link', 'href',
                        'date', 'time', 'location', 'address', 'phone', 'email', 'contact',
                        'rating', 'review', 'score', 'count', 'quantity', 'amount', 'number',
                        'currency', 'cost', 'fee', 'discount', 'sale', 'offer',
                        'status', 'state', 'condition', 'availability', 'stock',
                        'category', 'type', 'tag', 'genre', 'classification',
                        'brand', 'model', 'sku', 'product', 'item', 'article',
                        'description', 'summary', 'content', 'text', 'body',
                        'author', 'creator', 'publisher', 'source',
                        'size', 'dimension', 'weight', 'length', 'width', 'height',
                        'color', 'material', 'specification', 'feature'
                    ]
                    
                    # Keep the data attribute if it matches useful patterns
                    if any(pattern in data_key.lower() for pattern in useful_data_patterns):
                        continue
                
                # If we get here, check if it's in our removal list
                if attr_name in self.remove_attributes:
                    attributes_to_remove.append(attr_name)
            
            # Remove the identified attributes
            for attr_name in attributes_to_remove:
                if attr_name in element.attrs:
                    del element.attrs[attr_name]
                    removed_count += 1
        
        total_attributes_after = sum(len(el.attrs) for el in soup.find_all(lambda tag: tag.attrs))
        
        self.logger.info(f"Removed {removed_count} non-essential attributes "
                        f"({total_attributes_before} → {total_attributes_after})")
        
        return soup
    
    def _save_cleaned_html(self, url, html_content, stage):
        """Save cleaned HTML at different stages to temp folder for debugging"""
        try:
            if url:
                parsed_url = urlparse(url)
                domain = parsed_url.netloc.replace('www.', '').replace('.', '_')
            else:
                domain = "unknown"
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{domain}_{timestamp}_{stage}.html"
            filepath = os.path.join(self.cleaned_html_dir, filename)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            self.logger.debug(f"Cleaned HTML ({stage}) saved to: {filepath}")
            return filepath
        except Exception as e:
            self.logger.warning(f"Failed to save cleaned HTML: {e}")
            return None

    def clean_html(self, html_content, url=None, save_temp=True):
        """
        Main method to clean HTML content:
        1. Remove noise (scripts, styles, comments)
        2. Remove headers and footers
        3. Focus on main content
        4. Remove repeating structures (keep samples)
        5. Limit select tags to 2 option tags
        6. Remove empty div elements recursively
        7. Remove non-essential HTML attributes
        8. Remove whitespace and newlines between consecutive tags
        """
        self.logger.info("Starting HTML cleaning process...")
        
        soup = BeautifulSoup(html_content, 'html.parser')
        original_length = len(str(soup))
        
        # Step 1: Remove noise
        soup = self.remove_noise(soup)
        step1_html = str(soup)
        self.logger.info(f"Removed noise. Length: {len(step1_html)}")
        if save_temp:
            self._save_cleaned_html(url, step1_html, "01_removed_noise")
        
        # Step 2: Remove headers and footers
        soup = self.remove_header_footer(soup)
        step2_html = str(soup)
        self.logger.info(f"Removed headers/footers. Length: {len(step2_html)}")
        if save_temp:
            self._save_cleaned_html(url, step2_html, "02_removed_header_footer")
        
        # Step 3: Focus on main content
        soup = self.focus_on_main_content(soup)
        step3_html = str(soup)
        self.logger.info(f"Focused on main content. Length: {len(step3_html)}")
        if save_temp:
            self._save_cleaned_html(url, step3_html, "03_main_content")
        
        # Step 4: Remove repeating structures (keep samples)
        soup = self.remove_repeating_structures(soup, min_keep=2, min_total=3)
        step4_html = str(soup)
        self.logger.info(f"Removed repeating structures. Length: {len(step4_html)}")
        if save_temp:
            self._save_cleaned_html(url, step4_html, "04_removed_repeating_structures")
        
        # Step 5: Limit select options to 2
        soup = self.limit_select_options(soup, max_options=2)
        step5_html = str(soup)
        self.logger.info(f"Limited select options. Length: {len(step5_html)}")
        if save_temp:
            self._save_cleaned_html(url, step5_html, "05_limited_select_options")
        
        # Step 6: Remove empty divs recursively
        soup = self.remove_empty_divs_recursive(soup)
        step6_html = str(soup)
        self.logger.info(f"Removed empty divs. Length: {len(step6_html)}")
        if save_temp:
            self._save_cleaned_html(url, step6_html, "06_removed_empty_divs")
        
        # Step 7: Remove non-essential HTML attributes
        soup = self.remove_non_essential_attributes(soup)
        step7_html = str(soup)
        self.logger.info(f"Removed non-essential attributes. Length: {len(step7_html)}")
        if save_temp:
            self._save_cleaned_html(url, step7_html, "07_removed_attributes")
        
        # Step 8: Remove whitespace between consecutive tags
        step8_html = self.remove_whitespace_between_tags(step7_html)
        if save_temp:
            self._save_cleaned_html(url, step8_html, "08_removed_whitespace")
        
        final_html = step8_html
        final_length = len(final_html)
        if save_temp:
            self._save_cleaned_html(url, final_html, "09_final_cleaned")
        
        self.logger.info(f"HTML cleaning completed. Original: {original_length}, Final: {final_length}")
        self.logger.info(f"Reduction: {((original_length - final_length) / original_length * 100):.1f}%")
        
        return final_html