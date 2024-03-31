from htmlnode import HTMLNode, LeafNode, ParentNode
from textnode import TextNode

import re


class TextTypes:
    text = "text"
    bold = "bold"
    italic = "italic"
    code = "code"
    link = "link"
    image = "image"


def text_node_to_html_node(text_node):
    match text_node.text_type:
        case TextTypes.text:
            return LeafNode(None, text_node.text)
        case TextTypes.bold:
            return LeafNode("b", text_node.text)
        case TextTypes.italic:
            return LeafNode("i", text_node.text)
        case TextTypes.code:
            return LeafNode("code", text_node.text)
        case TextTypes.link:
            return LeafNode("a", text_node.text, {"href": text_node.url})
        case TextTypes.image:
            return LeafNode("img", None, {"src": text_node.url,
                                          "alt": text_node.text})
        case _:
            raise ValueError("Invalid Text Type")


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if isinstance(node, TextNode) and node.text_type == TextTypes.text:
            text = node.text
            parts = text.split(delimiter)
            #See how many parts we have
            #Len of parts must be odd to have a delimiter pair
            if len(parts) % 2 == 0:
                raise ValueError("Delimiter without pair")
            else:
                for i, part in enumerate(parts):
                    if i % 2 == 0:
                        if part != "":
                            new_nodes.append(TextNode(part, TextTypes.text))
                    else:
                        new_nodes.append(TextNode(part, text_type))


        else:
            new_nodes.append(node)
    return new_nodes


def extract_markdown_images(text):
    # ![text](url)
    match = re.findall(r"!\[(.*?)\]\((.*?)\)", text)
    results = []

    if match is None:
        return []

    for m in match:
        results.append(tuple([m[0], m[1]]))
    
    return results


def extract_markdown_links(text):
    # [text](url)
    match = re.findall(r"\[(.*?)\]\((.*?)\)", text)
    if match is None:
        return []
    results = []

    for m in match:
        results.append(tuple([m[0], m[1]]))
    
    return results


def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if isinstance(node, TextNode) and node.text_type == TextTypes.text:
            text = node.text
            images = extract_markdown_images(text)
            if images == []:
                new_nodes.append(node)
            else:
                end_text = text
                for image in images:
                    textsplit = end_text.split(f"![{image[0]}]({image[1]})", 1)
                    end_text = textsplit[-1]
                    if (textsplit[0] != ""):
                        new_nodes.append(TextNode(textsplit[0], TextTypes.text))
                    new_nodes.append(TextNode(image[0], TextTypes.image, image[1]))
                if (end_text != ""):
                    new_nodes.append(TextNode(end_text, TextTypes.text))
        else:
            if (node.text != ""):
                new_nodes.append(node)
    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if isinstance(node, TextNode) and node.text_type == TextTypes.text:
            text = node.text
            links = extract_markdown_links(text)
            if links == []:
                new_nodes.append(node)
            else:
                end_text = text
                for link in links:
                    textsplit = end_text.split(f"[{link[0]}]({link[1]})", 1)
                    end_text = textsplit[-1]
                    if (textsplit[0] != ""):
                        new_nodes.append(TextNode(textsplit[0], TextTypes.text))
                    new_nodes.append(TextNode(link[0], TextTypes.link, link[1]))
                if (end_text != ""):
                    new_nodes.append(TextNode(end_text, TextTypes.text))
        else:
            if (node.text != ""):
                new_nodes.append(node)
    return new_nodes

def text_to_textnodes(text):
    text_nodes = [TextNode(text, TextTypes.text)]
    try:
        text_nodes = split_nodes_delimiter(text_nodes, "**", TextTypes.bold)
        text_nodes = split_nodes_delimiter(text_nodes, "*", TextTypes.italic)
        text_nodes = split_nodes_delimiter(text_nodes, "`", TextTypes.code)
        text_nodes = split_nodes_image(text_nodes)
        text_nodes = split_nodes_link(text_nodes)
    except ValueError as e:
        print("Error: ", e)
        pass

    return text_nodes