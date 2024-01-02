#pragma once

#include <string>
#include <memory>
#include <vector>
#include <string_view>
#include <iostream>
#include <regex>

#include "Types.h"

class Trie
{
public:
    Trie();
    Trie(const Trie& trie) = default;
    ~Trie() = default;

    /* functions */
    void insert(const std::string_view& word) noexcept;
    bool search(const std::string_view& word) const noexcept;
    void print() const noexcept;
    void match(const std::string& pattern, const std::string& order) const noexcept;
    std::vector<std::string> allStrings(const std::string from, const std::string to) const noexcept;

private:
    struct Node 
    {
        Node() : m_isLeaf(false), m_data(static_cast<char>(Characters::UNDEFINED_CHARACTER)),
             m_children() { }
        Node(const char data) : m_data(data), m_isLeaf(false), m_children() { }

        /* functions */
        void print(std::string& buffer, const std::string prefix, const std::string childrenPrefix) const noexcept
        {
            buffer += prefix + m_data + '\n';

            for(const auto& it : m_children)
            {
                if(!it.m_isLeaf)
                {
                    it.print(buffer, childrenPrefix + "├── ", childrenPrefix + "│   ");
                }
                else
                {
                    it.print(buffer, childrenPrefix + "└── ", childrenPrefix + "    ");
                }
            }
        }

    void allStrings(const std::string& from, const std::string& to, const std::string& word, std::vector<std::string>& words) const noexcept
    {
        if(m_isLeaf)
        {
            if( ( (word.compare(to) <= 0) || (to == "")) && ((word.compare(from) >= 0) || (from == "")) )
            {
                words.push_back(word);
            }
        }
    
        for(const auto& it : m_children)
        {   
            it.allStrings(from, to, word + it.m_data, words);
        }
    }

    void match(int position, std::string word, std::vector<std::string>& words, const std::string& pattern) const noexcept
    {
        if(position > pattern.size())
            return;

        if(m_isLeaf && (position == pattern.size() || pattern[position] == '*'))
        {
            words.push_back(word);
        }

        if(pattern[position] == '?')
        {
            for(const auto& it : m_children)
            {
                it.match(position + 1, word + it.m_data, words, pattern);
            }
        }
        else if(pattern[position] == '*')
        {
            for(const auto& it : m_children)
            {
                it.match(position, word + it.m_data, words, pattern);
            }
        }
        else
        {
            auto iter = std::find_if(m_children.begin(), m_children.end(), [&](const auto& node)
            {
                return node.m_data == pattern[position];  
            });

            if(iter != m_children.end())
            {
                iter->match(position + 1, word + iter->m_data, words, pattern);
            }
        }
    }


        /* members */
        char m_data;
        std::vector<Node> m_children;
        bool m_isLeaf;
    };
    /* -------------------------------- */

    /* members */
    std::shared_ptr<Node> m_root;
};