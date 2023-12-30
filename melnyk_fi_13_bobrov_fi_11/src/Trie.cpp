#include "../include/Trie.h"

Trie::Trie() 
{
    m_root = std::make_shared<Node>();
}

void Trie::insert(const std::string_view& word) noexcept
{
    auto tempNode = m_root.get();
    for(const auto& symbol : word)
    {
        auto iter = std::find_if(tempNode->m_children.begin(), tempNode->m_children.end(), [&symbol](const auto& node)
        {
            return node.m_data == symbol;  
        });

        if(iter == tempNode->m_children.end())
        {
            tempNode->m_children.push_back(Node(symbol));
            tempNode = &tempNode->m_children.back();
        }
        else
        {
            tempNode = &(*iter);
        }
    }

    tempNode->m_isLeaf = true;
}

bool Trie::search(const std::string_view& word) const noexcept
{
    auto tempNode = m_root.get();
    for(const auto& symbol : word)
    {
        auto iter = std::find_if(tempNode->m_children.begin(), tempNode->m_children.end(), [&symbol](const auto& node)
        {
            return node.m_data == symbol;  
        });

        if(iter != tempNode->m_children.end())
        {
            tempNode = &(*iter);
        }
        else
        {
            return false;
        }
    }

    if(tempNode->m_data != static_cast<char>(Characters::UNDEFINED_CHARACTER) && 
        tempNode->m_isLeaf)
    {
        return true;
    }
    return false;
}

std::vector<std::string> Trie::allStrings() const noexcept
{
    std::vector<std::string> strings;
    m_root->allStrings("", strings);
    return strings;
}

void Trie::print() const noexcept
{
    std::string result;
    m_root->print(result, "", "");
    std::cout << result << std::endl;
}